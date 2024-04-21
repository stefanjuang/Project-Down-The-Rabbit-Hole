import asyncio
import os
from os.path import dirname, join

import xai_sdk
from dotenv import load_dotenv

# Load environment variables
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(verbose=True, dotenv_path=dotenv_path)
XAI_API_KEY = os.environ.get("XAI_API_KEY")


#     preamble = """\
# This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

# Human: I want you to find the oldest person from a list of people. Each person is a tuple (name, age).

# Please format your answer as a valid JSON. For eg. if the answer is (Bob, 50), your output should be.

# {
#     name: "Bob",
#     age: 50
# }<|separator|>

# Assistant: Understood! Please provide the list of people as a list of (name, age) pairs."""


class GrokClient:
    def __init__(self):
        self.client = xai_sdk.Client()
        self.sampler = self.client.sampler

    async def get_insights(self, topic_name, text):
        PREAMBLE = f"""\
            This is a summary and analysis of the topic '{topic_name}' based on relevant tweets. Grok will analyze the content and generate a comprehensive view on the subject matter.
            
            Generate a comprehensive and informative answer solely based on topic and relevant tweets of {"Elon Musk"}. Combine inputs together into a coherent answer. Do not repeat text. Cite search results using [$`{number}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. [2][3][4][5]
            """

        prompt = (
            PREAMBLE
            + f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant: "
            + "{\n"
        )

        insights = ""
        async for token in self.sampler.sample(
            prompt=prompt,
            max_len=1024,
            stop_tokens=["<|separator|>"],
            temperature=0.5,
            nucleus_p=0.95,
        ):
            insights += token.token_str
        return insights


async def main():
    grok_client = GrokClient(api_key=XAI_API_KEY)
    text = input("Write a message: ")
    insights = await grok_client.get_insights("topic_name", text)
    print(insights)


if __name__ == "__main__":
    asyncio.run(main())
