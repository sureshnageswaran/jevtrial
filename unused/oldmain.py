from dotenv import load_dotenv
load_dotenv()

import asyncio
from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score

async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
            state={"document": "I have been a premium user for 2 years now. My friend's mind was blown by the dashboard view and he also wants to sign up for a new account for business. What do I do?"},
            # state={"document": "I selected the premium plan for personal account setup, and now I want to setup a another new account for business. What do I do?"},
            # state={"document": "I selected the premium plan during account setup, but the dashboard still says I'm a free user. What do I do?"},
            # state={"document": "I’m trying to set up the premium analytics package, but the dashboard says my account isn’t eligible. Who do I talk to?"},
            # state={"document": "I’m trying to set up the premium analytics package, but the dashboard says my account isn’t eligible. Who do I talk to?"}, 
            # state={"document": "I was charged for my order of chewing gum and instead received a television. Do I return it?"},
            questions={
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
            },            
        )

    print (response.choices["issue_type"].choice)
    print (response.nouls["billing"].noul)
    print (response.choices["tone"].choice)
    print (response.scores["urgency"].score)    


asyncio.run(main())

