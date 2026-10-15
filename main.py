"""Run the private-credit monitoring cases against Jev and Cloudflare Clef.

Required environment variables:
  TYPESAFE_API_KEY             Jev API key (as required by typesafe_sdk)
  CLOUDFLARE_ACCOUNT_ID        Cloudflare account ID
  CLOUDFLARE_AUTH_TOKEN        Cloudflare API token with Workers AI access

Optional:
  CLOUDFLARE_MODEL             @cf/cloudflare/clef (default) or
                               @cf/cloudflare/clef-flash

Latency is measured around each model request, including network/API time and
excluding local case loading and result printing. Expected labels and rationales
are deliberately excluded from both model requests.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
import os
import statistics
import time
from pathlib import Path
from typing import Any

import requests
from typesafe_sdk import AsyncTypeSafeClient, Choice

CASES_FILE = Path(__file__).with_name("tests.json")
CLOUDFLARE_MODEL = os.getenv("CLOUDFLARE_MODEL", "@cf/cloudflare/clef")
CLOUDFLARE_TIMEOUT_SECONDS = 60

ACTION_CHOICES = {
    "no_action": "No action is warranted under the supplied agreement, facts, workflow context, and policy.",
    "covenant_test": "Perform or complete the documented covenant calculation or test.",
    "borrower_follow_up": "Request missing, unclear, inconsistent, late, or corrected information from the borrower or its agent.",
    "counsel_review": "Refer a question about agreement interpretation, legal rights, notice, waiver, default, or cure to counsel.",
    "credit_review": "Escalate a verified breach, material deterioration, or policy-defined risk trigger to the credit team.",
}

QUESTION_INSTRUCTIONS = (
    "Choose the single next workflow action for private-credit monitoring. "
    "Use only the supplied observed fact, evidence status, agreement terms, "
    "workflow context, and policy. Select the earliest appropriate next step. "
    "A reported metric is not a verified breach: use covenant_test when a "
    "documented calculation remains to be performed; use borrower_follow_up "
    "when required information is missing, unclear, inconsistent, or late; "
    "use counsel_review for a genuine legal interpretation or rights question; "
    "use credit_review only for a verified breach, material deterioration, "
    "or explicit policy trigger. Do not decide that a default legally occurred, "
    "and do not infer terms that are not supplied. Use no_action only when "
    "the supplied policy calls for no further step."
)

# Jev SDK schema.
JEV_QUESTIONS = {
    "next_action": Choice(
        instructions=QUESTION_INSTRUCTIONS,
        criteria=ACTION_CHOICES,
    )
}

# Cloudflare Workers AI uses its own JSON schema for the same semantic question.
CLEF_QUESTIONS = {
    "next_action": {
        "type": "choice",
        "instructions": QUESTION_INSTRUCTIONS,
        "criteria": ACTION_CHOICES,
    }
}


def load_cases() -> list[dict[str, Any]]:
    with CASES_FILE.open(encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("tests.json must contain a JSON list of cases.")
    required = {"id", "state", "expected_action"}
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict) or not required.issubset(case):
            raise ValueError(f"Case {index} must contain {sorted(required)}.")
        if not isinstance(case["state"], dict):
            raise ValueError(f"Case {index} 'state' must be an object.")
        if case["expected_action"] not in ACTION_CHOICES:
            raise ValueError(f"Case {index} has an unknown expected_action.")
    return cases


def extract_clef_choice(payload: dict[str, Any]) -> tuple[str | None, Any]:
    """Return selected choice and the raw answer object from Workers AI output."""
    result = payload.get("result", payload)
    answers = result.get("answers", {}) if isinstance(result, dict) else {}
    answer = answers.get("next_action") if isinstance(answers, dict) else None

    # Some API/model revisions may wrap the selected option differently.
    if isinstance(answer, str):
        return answer, answer
    if isinstance(answer, dict):
        for key in ("choice", "answer", "label", "value"):
            value = answer.get(key)
            if isinstance(value, str):
                return value, answer
        # If only per-option probabilities are returned, use the largest one.
        probs = answer.get("probabilities")
        if isinstance(probs, dict) and probs:
            return max(probs, key=probs.get), answer
        # Occasionally the answer itself may be a probability map.
        numeric = {k: v for k, v in answer.items() if isinstance(v, (int, float))}
        if numeric and set(numeric).issubset(ACTION_CHOICES):
            return max(numeric, key=numeric.get), answer
    return None, answer


def cloudflare_request_sync(state: dict[str, Any], model: str = CLOUDFLARE_MODEL) -> dict[str, Any]:
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
    if not account_id or not auth_token:
        raise RuntimeError(
            "Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_AUTH_TOKEN in your environment or .env file."
        )

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{model}"
    )
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "model": "clef-flash" if "clef-flash" in model else "clef",
            "state": state,
            "questions": CLEF_QUESTIONS,
        },
        timeout=CLOUDFLARE_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("success") is False:
        raise RuntimeError(f"Cloudflare API returned success=false: {payload.get('errors')}")
    return payload


async def call_clef(
    state: dict[str, Any], model: str = CLOUDFLARE_MODEL
) -> tuple[str | None, float, Any, str | None]:
    start = time.perf_counter()
    try:
        payload = await asyncio.to_thread(cloudflare_request_sync, state, model)
        elapsed_ms = (time.perf_counter() - start) * 1000
        choice, raw_answer = extract_clef_choice(payload)
        if choice is None:
            return None, elapsed_ms, raw_answer, "Could not find next_action in Cloudflare response"
        return choice, elapsed_ms, raw_answer, None
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return None, elapsed_ms, None, f"{type(exc).__name__}: {exc}"


def observed_description(state: dict[str, Any]) -> str:
    observed = state.get("observed_fact", {})
    return str(observed.get("description", "(no observed_fact.description field)"))


async def main() -> None:
    cases = load_cases()
    if not cases:
        print("No cases found in tests.json.")
        return

    cloudflare_ready = bool(os.getenv("CLOUDFLARE_ACCOUNT_ID") and os.getenv("CLOUDFLARE_AUTH_TOKEN"))
    if not cloudflare_ready:
        print("Cloudflare calls will be skipped: set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_AUTH_TOKEN.")

    stats: dict[str, dict[str, Any]] = {
        "Jev": {"correct": 0, "completed": 0, "latencies": []},
        "Clef": {"correct": 0, "completed": 0, "latencies": []},
    }

    async with AsyncTypeSafeClient() as client:
        for case in cases:
            expected = case["expected_action"]
            state = case["state"]
            print(f"\n--- {case['id']} ---")
            print(f"Observed fact: {observed_description(state)}")
            print(f"Expected action: {expected}")

            # Jev
            started = time.perf_counter()
            try:
                response = await client.system_one(state=state, questions=JEV_QUESTIONS)
                jev_ms = (time.perf_counter() - started) * 1000
                jev_action = response.choices["next_action"].choice
                stats["Jev"]["completed"] += 1
                stats["Jev"]["latencies"].append(jev_ms)
                jev_match = jev_action == expected
                stats["Jev"]["correct"] += int(jev_match)
                print(f"Jev:  {jev_action} | {jev_ms:.1f} ms | {'MATCH' if jev_match else 'MISS'}")
            except Exception as exc:
                jev_ms = (time.perf_counter() - started) * 1000
                print(f"Jev:  ERROR | {jev_ms:.1f} ms | {type(exc).__name__}: {exc}")

            # Cloudflare Clef / Clef-Flash
            if cloudflare_ready:
                clef_action, clef_ms, raw_answer, error = await call_clef(state)
                if error:
                    print(f"Clef: ERROR | {clef_ms:.1f} ms | {error}")
                    if raw_answer is not None:
                        print(f"      Raw answer: {raw_answer}")
                else:
                    stats["Clef"]["completed"] += 1
                    stats["Clef"]["latencies"].append(clef_ms)
                    clef_match = clef_action == expected
                    stats["Clef"]["correct"] += int(clef_match)
                    print(f"Clef: {clef_action} | {clef_ms:.1f} ms | {'MATCH' if clef_match else 'MISS'}")
                    if isinstance(raw_answer, dict) and "probabilities" in raw_answer:
                        print(f"      Probabilities: {raw_answer['probabilities']}")

    print("\n=== Summary ===")
    for model, result in stats.items():
        if model == "Clef" and not cloudflare_ready:
            continue
        completed = result["completed"]
        if completed:
            latencies = result["latencies"]
            print(
                f"{model}: {result['correct']}/{completed} correct "
                f"({result['correct'] / completed:.1%}); "
                f"mean {statistics.mean(latencies):.1f} ms; "
                f"median {statistics.median(latencies):.1f} ms"
            )
        else:
            print(f"{model}: no successful responses")


if __name__ == "__main__":
    asyncio.run(main())
