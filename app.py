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

from main import ACTION_CHOICES, JEV_QUESTIONS, call_clef, load_cases, observed_description

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
        response = await client.system_one(state=state, questions=JEV_QUESTIONS)
        ms = (time.perf_counter() - start) * 1000
        return ProviderResult(choice=response.choices["next_action"].choice, ms=ms)
    except Exception as exc:
        ms = (time.perf_counter() - start) * 1000
        return ProviderResult(choice=None, ms=ms, error=f"{type(exc).__name__}: {exc}")


async def run_clef_flash(_client: AsyncTypeSafeClient | None, state: dict[str, Any]) -> ProviderResult:
    choice, ms, raw, error = await call_clef(state, CLEF_FLASH_MODEL)
    return ProviderResult(choice=choice, ms=ms, raw=raw, error=error)


# Future providers (e.g. OpenAI) go here.
PROVIDERS = [
    Provider("Jev", run_jev),
    Provider("Clef-flash", run_clef_flash),
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


def match_label(result: ProviderResult | None, expected: str) -> str:
    if result is None:
        return "–"
    if result.error:
        return "Error"
    return "✅ Match" if result.choice == expected else "❌ Miss"


def build_table(cases: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for case in cases:
        case_results = st.session_state.results.get(case["id"], {})
        row = {"Case": case["id"], "Expected": case["expected_action"]}
        for provider in PROVIDERS:
            result = case_results.get(provider.name)
            row[f"{provider.name}"] = match_label(result, case["expected_action"])
            row[f"{provider.name} time"] = f"{result.ms:,.0f} ms" if result else "–"
        rows.append(row)
    return pd.DataFrame(rows)


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


def render_case_detail(case: dict[str, Any]) -> None:
    st.subheader(case["id"])
    st.markdown(f"**Observed fact:** {observed_description(case['state'])}")
    st.markdown(f"**Expected action:** `{case['expected_action']}`")
    if case.get("rationale"):
        with st.expander("Rationale"):
            st.write(case["rationale"])

    case_results = st.session_state.results.get(case["id"], {})
    if not case_results:
        st.info("No results for this case yet. Use **Run selected** or **Run all cases**.")
        return

    for provider in PROVIDERS:
        result = case_results.get(provider.name)
        with st.container(border=True):
            header, timing = st.columns([3, 2])
            header.markdown(f"**{provider.name}**")
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
                st.caption("Probabilities")
                st.bar_chart(pd.Series(result.raw["probabilities"]).reindex(list(ACTION_CHOICES)).fillna(0))
            if result.raw is not None:
                with st.expander("Raw response"):
                    st.json(result.raw, expanded=False)


def main() -> None:
    st.set_page_config(page_title="Private-credit benchmark", layout="wide")
    st.title("Private-credit monitoring benchmark")
    st.caption("Next-action decisions from Jev and Cloudflare Clef-flash, with timings.")

    cases = load_cases()
    st.session_state.setdefault("results", {})
    st.session_state.setdefault("run_seconds", None)

    selected_index = st.session_state.get("selected_case", 0)
    controls = st.columns([1, 1, 4])
    if controls[0].button("▶ Run all cases", type="primary", width="stretch"):
        run_cases(cases, "Running all cases")
    if controls[1].button("▶ Run selected", width="stretch"):
        run_cases([cases[selected_index]], f"Running {cases[selected_index]['id']}")
    if st.session_state.run_seconds is not None:
        controls[2].caption(f"Last run took {st.session_state.run_seconds:,.1f} s wall-clock")

    render_summary(cases)
    st.divider()

    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown("**Cases** — click a row to see its results")
        event = st.dataframe(
            build_table(cases),
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
            width="stretch",
            key="case_table",
        )
        selected_rows = event.selection.rows if event and event.selection else []
        if selected_rows:
            st.session_state.selected_case = selected_rows[0]
            selected_index = selected_rows[0]
    with right:
        render_case_detail(cases[selected_index])


if __name__ == "__main__":
    main()
