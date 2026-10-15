"""Live Streamlit UI for the private-credit monitoring benchmark.

Run with:  uv run streamlit run app.py

To add another model, write an async function that returns a ProviderResult
and append a Provider to PROVIDERS below.
"""
import asyncio
import statistics
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

import pandas as pd
import streamlit as st
from typesafe_sdk import AsyncTypeSafeClient

from main import call_clef, call_luna, case_actions, jev_questions, load_cases, observed_description

CLEF_FLASH_MODEL = "@cf/cloudflare/clef-flash"


@dataclass
class ProviderResult:
    choice: str | None
    ms: float
    raw: Any = None
    error: str | None = None


@dataclass
class Provider:
    name: str
    run: Callable[[AsyncTypeSafeClient | None, dict[str, Any]], Awaitable[ProviderResult]]


async def run_jev(client: AsyncTypeSafeClient | None, state: dict[str, Any]) -> ProviderResult:
    start = time.perf_counter()
    try:
        if client is None:
            raise RuntimeError("Jev client could not be created. Check TYPESAFE_API_KEY.")
        response = await client.system_one(state=state, questions=jev_questions(state))
        ms = (time.perf_counter() - start) * 1000
        answer = response.choices["next_action"]
        raw = {
            **answer.model_dump(mode="json"),
            "model": response.model,
            "usage": response.usage.model_dump(mode="json"),
        }
        return ProviderResult(choice=answer.choice, ms=ms, raw=raw)
    except Exception as exc:
        ms = (time.perf_counter() - start) * 1000
        return ProviderResult(choice=None, ms=ms, error=f"{type(exc).__name__}: {exc}")


async def run_clef_flash(_client: AsyncTypeSafeClient | None, state: dict[str, Any]) -> ProviderResult:
    choice, ms, raw, error = await call_clef(state, CLEF_FLASH_MODEL)
    return ProviderResult(choice=choice, ms=ms, raw=raw, error=error)


async def run_luna(_client: AsyncTypeSafeClient | None, state: dict[str, Any]) -> ProviderResult:
    choice, ms, raw, error = await call_luna(state)
    return ProviderResult(choice=choice, ms=ms, raw=raw, error=error)


PROVIDERS = [
    Provider("Jev", run_jev),
    Provider("Clef-flash", run_clef_flash),
    Provider("OpenAI Luna", run_luna),
]


async def _run_cases(cases: list[dict[str, Any]], on_result: Callable[[int, str, ProviderResult], None]) -> None:
    client: AsyncTypeSafeClient | None = None
    try:
        client = AsyncTypeSafeClient()
        await client.__aenter__()
    except Exception:
        client = None
    try:
        for index, case in enumerate(cases):
            for provider in PROVIDERS:
                result = await provider.run(client, case["state"])
                on_result(index, provider.name, result)
    finally:
        if client is not None:
            await client.__aexit__(None, None, None)


def run_cases(cases: list[dict[str, Any]], progress_text: str) -> None:
    """Run the given cases through every provider, storing results in session state."""
    results = st.session_state.results
    bar = st.progress(0.0, text=progress_text)
    total = len(cases) * len(PROVIDERS)
    done = 0

    def record(index: int, provider_name: str, result: ProviderResult) -> None:
        nonlocal done
        results.setdefault(cases[index]["id"], {})[provider_name] = result
        done += 1
        bar.progress(done / total, text=f"{progress_text} ({done}/{total})")

    started = time.perf_counter()
    asyncio.run(_run_cases(cases, record))
    st.session_state.run_seconds = time.perf_counter() - started
    bar.empty()


def status_icon(result: ProviderResult | None, expected: str) -> str:
    if result is None:
        return "⚪"
    if result.error:
        return "⚠️"
    return "✅" if result.choice == expected else "❌"


def case_label(case: dict[str, Any]) -> str:
    case_results = st.session_state.results.get(case["id"], {})
    icons = "".join(status_icon(case_results.get(p.name), case["expected_action"]) for p in PROVIDERS)
    return f"{icons}  {case['id']}"


def summary_stats(cases: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stats = {}
    for provider in PROVIDERS:
        correct = completed = 0
        latencies: list[float] = []
        total_ms = 0.0
        for case in cases:
            result = st.session_state.results.get(case["id"], {}).get(provider.name)
            if result is None:
                continue
            total_ms += result.ms
            if result.error:
                continue
            completed += 1
            latencies.append(result.ms)
            correct += int(result.choice == case["expected_action"])
        stats[provider.name] = {
            "correct": correct,
            "completed": completed,
            "mean": statistics.mean(latencies) if latencies else None,
            "median": statistics.median(latencies) if latencies else None,
            "total_ms": total_ms,
        }
    return stats


def render_summary(cases: list[dict[str, Any]]) -> None:
    stats = summary_stats(cases)
    columns = st.columns(len(PROVIDERS))
    for column, provider in zip(columns, PROVIDERS):
        s = stats[provider.name]
        with column:
            if s["completed"]:
                st.metric(
                    f"{provider.name} accuracy",
                    f"{s['correct']}/{s['completed']}",
                    f"{s['correct'] / s['completed']:.0%}",
                    delta_color="off",
                )
                st.caption(
                    f"Mean {s['mean']:,.0f} ms · Median {s['median']:,.0f} ms · "
                    f"Total {s['total_ms'] / 1000:,.1f} s"
                )
            else:
                st.metric(f"{provider.name} accuracy", "–")
                st.caption("No results yet")


def humanize(key: str) -> str:
    return key.replace("_", " ").capitalize()


def render_fields(fields: dict[str, Any]) -> None:
    for key, value in fields.items():
        if isinstance(value, bool):
            value = "Yes" if value else "No"
        st.markdown(f"- **{humanize(key)}:** {value}")


def render_results(case: dict[str, Any]) -> None:
    st.subheader("Results")

    case_results = st.session_state.results.get(case["id"], {})
    if not case_results:
        st.info("No results for this test yet. Use **Run this test** or **Run all tests**.")
        return

    for column, provider in zip(st.columns(len(PROVIDERS)), PROVIDERS):
        result = case_results.get(provider.name)
        with column, st.container(border=True):
            name, timing = st.columns([3, 2])
            name.markdown(f"**{provider.name}**")
            if result is None:
                st.caption("Not run yet")
                continue
            timing.markdown(f"⏱️ **{result.ms:,.0f} ms**")
            if result.error:
                st.error(result.error)
                continue
            if result.choice == case["expected_action"]:
                st.success(f"Chose `{result.choice}` — matches expected")
            else:
                st.warning(f"Chose `{result.choice}` — expected `{case['expected_action']}`")
            if isinstance(result.raw, dict) and result.raw.get("probabilities"):
                actions = case_actions(case["state"])
                st.caption("Probabilities")
                st.bar_chart(
                    pd.Series(result.raw["probabilities"]).reindex(actions).fillna(0),
                    horizontal=True,
                    height=max(180, 24 * len(actions)),
                )
            if result.raw is not None:
                with st.expander("Raw response"):
                    st.json(result.raw, expanded=False)


def render_explanation(case: dict[str, Any]) -> None:
    state = case["state"]
    st.subheader("About this test")
    st.markdown(f"**{case['id']}**")
    meta = [state.get(k) for k in ("borrower", "facility", "as_of") if state.get(k)]
    if meta:
        st.caption(" · ".join(meta))
    st.markdown(f"**Observed fact:** {observed_description(state)}")
    st.markdown(f"**Expected action:** `{case['expected_action']}`")
    if case.get("rationale"):
        st.markdown(f"**Why:** {case['rationale']}")

    sections = [
        ("Observed fact details", state.get("observed_fact")),
        ("Agreement terms", state.get("agreement_terms")),
        ("Workflow context", state.get("workflow_context")),
        ("Policy", state.get("policy")),
    ]
    for title, fields in sections:
        if isinstance(fields, dict) and fields:
            with st.expander(title):
                render_fields(fields)


def main() -> None:
    st.set_page_config(page_title="Private Markets Middle Office | Decision Models Benchmark", layout="wide")
    st.title("Private Markets Middle Office | Decision Models Benchmark")
    st.caption("Next-action decisions from Jev, Cloudflare Clef-flash, and OpenAI Luna, with timings.")

    cases = load_cases()
    st.session_state.setdefault("results", {})
    st.session_state.setdefault("run_seconds", None)

    left, right = st.columns([1, 2], gap="large")

    with left:
        if st.button("▶ Run all tests", type="primary", width="stretch"):
            run_cases(cases, "Running all tests")
        if st.session_state.run_seconds is not None:
            st.caption(f"Last run took {st.session_state.run_seconds:,.1f} s wall-clock")
        render_summary(cases)
        st.divider()
        heading, button = st.columns([1, 1], vertical_alignment="center")
        heading.markdown("**Tests**")
        if button.button("▶ Run this test", type="primary", width="stretch"):
            # The radio below holds the selection; its value is already in session state.
            case = cases[st.session_state.get("selected_case", 0)]
            run_cases([case], f"Running {case['id']}")
            st.rerun()
        st.caption("Icons: " + " · ".join(p.name for p in PROVIDERS) + "  (✅ match, ❌ miss, ⚠️ error, ⚪ not run)")
        selected_index = st.radio(
            "Tests",
            range(len(cases)),
            format_func=lambda i: case_label(cases[i]),
            key="selected_case",
            label_visibility="collapsed",
        )

    case = cases[selected_index]
    with right:
        with st.container(border=True, height=480):
            render_results(case)
        with st.container(border=True, height=420):
            render_explanation(case)


if __name__ == "__main__":
    main()
