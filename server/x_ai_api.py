"""A simple example demonstrating text completion."""

import asyncio
import os
import sys
from os.path import dirname, join

import xai_sdk
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")

load_dotenv(verbose=True, dotenv_path=dotenv_path)
XAI_API_KEY = os.environ.get("XAI_API_KEY")


async def main():
    """Runs the example."""
    client = xai_sdk.Client()

    conversation = client.chat.create_conversation()

    print("Enter an empty message to quit.\n")

    while True:
        user_input = input("Human: ")
        print("")

        if not user_input:
            return

        token_stream, _ = conversation.add_response(user_input)
        print("Grok: ", end="")
        async for token in token_stream:
            print(token, end="")
            sys.stdout.flush()
        print("\n")


asyncio.run(main())
