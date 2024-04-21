import asyncio

import xai_sdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)


async def main():
    client = xai_sdk.Client()
    sampler = client.sampler

    PREAMBLE = """\
This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

Human: I want you to find the oldest person from a list of people. Each person is a tuple (name, age).

Please format your answer as a valid JSON. For eg. if the answer is (Bob, 50), your output should be.

{
    name: "Bob",
    age: 50
}<|separator|>

Assistant: Understood! Please provide the list of people as a list of (name, age) pairs."""

    # (Bob, 50), (John, 25), (Alice, 100)

    text = input("Write a message ")

    prompt = (
        PREAMBLE + f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant: " + "{\n"
    )
    print(prompt)
    async for token in sampler.sample(
        prompt=prompt,
        max_len=1024,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.95,
    ):
        print(token.token_str, end="")
    print()


if __name__ == "__main__":
    asyncio.run(main())
