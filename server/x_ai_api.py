"""A simple example demonstrating text completion."""

import asyncio
import os
from os.path import dirname, join

import xai_sdk
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")

load_dotenv(verbose=True, dotenv_path=dotenv_path)
XAI_API_KEY = os.environ.get("XAI_API_KEY")


async def main():
    """Runs the example."""
    client = xai_sdk.Client()

    prompt = "The answer to live and the universe is"
    print(prompt, end="")
    async for token in client.sampler.sample(prompt, max_len=3):
        print(token.token_str, end="")
    print("")


asyncio.run(main())
