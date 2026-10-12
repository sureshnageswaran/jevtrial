from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from pathlib import Path

from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score


CASES_FILE = Path(__file__).with_name("tests.json")


def load_cases() -> list[dict]:
    with CASES_FILE.open(encoding="utf-8") as file:
        cases = json.load(file)

    if not isinstance(cases, list):
        raise ValueError("cases.json must contain a JSON list of test cases.")

    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("document"), str):
            raise ValueError(
                f"Test case {index + 1} must be an object with a string 'document' field."
            )

    return cases


async def main() -> None:
    cases = load_cases()

    questions = {
        "issue_type": Choice(
            instructions="What type of issue is this about?",
            criteria={
                "sales": "Customer was sold a product or service and has a question or complaint about it.",
                "technical": "Customer is having a technical issue with a product or service.",
                "delivery": "Customer is having an issue with the delivery of a product or service.",
                "billing": "Customer is having an issue with billing or payment for a product or service.",
                "other": "Customer is having an issue that doesn't fit into the other categories.",
                "human": "Customer request is best served by a human agent and cannot be resolved by an AI assistant.",
            },
        ),
        "billing": Noul(instructions="Is this a ticket about billing?"),
        "tone": Choice(
            instructions="What is the tone of this customer?",
            criteria={"happy": None, "neutral": None, "frustrated": None, "angry": None},
        ),
        "urgency": Score(
            instructions="How urgent is this ticket?",
            criteria=["Same Day", "Up to 5 Business Days", "Up to 10 Business Days"],
        ),
    }

    async with AsyncTypeSafeClient() as client:
        for index, case in enumerate(cases, start=1):
            response = await client.system_one(
                state={"document": case["document"]},
                questions=questions,
            )

            case_id = case.get("id", f"case-{index}")
            print(f"\n--- {case_id} ---")
            print(f"Document: {case['document']}")
            print(f"Issue type: {response.choices['issue_type'].choice}")
            print(f"Billing: {response.nouls['billing'].noul}")
            print(f"Tone: {response.choices['tone'].choice}")
            print(f"Urgency: {response.scores['urgency'].score}")


if __name__ == "__main__":
    asyncio.run(main())