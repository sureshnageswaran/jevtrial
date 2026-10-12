"""Private-credit monitoring decision benchmark using the TypeSafe Jev SDK.

Each case in tests.json is sent as a state packet. The model selects the
appropriate next workflow action; expected_action is shown only after inference
for local evaluation and is never sent to the model.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from pathlib import Path
from typing import Any

from typesafe_sdk import AsyncTypeSafeClient, Choice

CASES_FILE = Path(__file__).with_name("tests.json")

ACTION_CHOICES = {
    "no_action": "No action is warranted under the supplied agreement, facts, workflow context, and policy.",
    "covenant_test": "Perform or complete the documented covenant calculation or test.",
    "borrower_follow_up": "Request missing, unclear, inconsistent, late, or corrected information from the borrower or its agent.",
    "counsel_review": "Refer a question about agreement interpretation, legal rights, notice, waiver, default, or cure to counsel.",
    "credit_review": "Escalate a verified breach, material deterioration, or policy-defined risk trigger to the credit team.",
}

QUESTIONS = {
    "next_action": Choice(
        instructions=(
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
        ),
        criteria=ACTION_CHOICES,
    )
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


async def main() -> None:
    cases = load_cases()
    correct = 0
    async with AsyncTypeSafeClient() as client:
        for case in cases:
            # Deliberately exclude expected_action and rationale from model input.
            response = await client.system_one(state=case["state"], questions=QUESTIONS)
            predicted = response.choices["next_action"].choice
            expected = case["expected_action"]
            matched = predicted == expected
            correct += int(matched)
            print(f"\n--- {case['id']} ---")
            print(f"Observed fact: {case['state']['observed_fact']['description']}")
            print(f"Expected action: {expected}")
            print(f"Model action:    {predicted}")
            print(f"Match:           {'YES' if matched else 'NO'}")
    print(f"\nExact matches: {correct}/{len(cases)} ({correct / len(cases):.1%})")


if __name__ == "__main__":
    asyncio.run(main())
