import asyncio
import os
from os.path import dirname, join

import xai_sdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)


PREAMBLE = """\
            You will analyze the content and generate a comprehensive insights givent the topic and relevant tweets of user.
            
            Generate a comprehensive and informative answer solely based on topic and relevant tweets of user. Combine inputs together into a coherent answer. Do not repeat text, do not ramble or yapping. Cite search results using [$`{index}`] notation. Cite the relevant tweets to the context correctly.
            with input
            {
                "user": "Elon Musk",
                "topic": "Grok AI",
                "tweets: [
                    {
                        "index": 1,
                        "text": "In a few weeks, we will add a “Grok, analysis!” button under 𝕏 posts",
                        "url": "https://x.com/elonmusk/status/1728591219180052652"
                        },
                        
                    {
                        "index": 2,
                        "text": "Colon Cologne, the fragrance that takes you beyond Uranus!” – Grok",
                        "url": "https://x.com/elonmusk/status/1751486972336492974"
                        },
                        {
                        "index": 3,
                        "text": "Grok, what’s your favorite sports team?In the coming weeks, Grok will summarize these mammoth laws before they are passed by Congress, so you know what their real purpose is",
                        "url": "https://x.com/elonmusk/status/1763433242047189232"
                        },
                ]
            }
            example output is to generate summary text of the insights with markdown format, show bullet points and respond concisely. index in tweets is link with [$`{index}`] in summary
            "Elon Musk's tweets about 'Grok AI' on X (formerly Twitter) unveil an innovative AI tool aimed at enhancing user interaction with online content. 
            - In his first tweet, Musk introduces the forthcoming 'Grok, analysis!' button, set to provide deep, intuitive insights into posts on the platform. This feature embodies the essence of 'grokking'—a term from Heinlein's science fiction, implying a profound, comprehensive understanding of a subject [1]
            - The second tweet introduces 'Colon Cologne,' a whimsical, fictional product from Grok, illustrating the AI's potential in generating creative and engaging content. This tweet reflects Musk's approach to integrating serious tech advancements with humor, potentially broadening Grok AI's appeal and application beyond conventional uses [2]
            - The third tweet reveals a more serious application of Grok AI, discussing its future role in summarizing complex legislation before its passage by Congress. This indicates Grok AI's utility in making intricate governmental processes transparent and understandable for the general public, thereby fostering informed citizenship [3]
            Overall, Musk's tweets showcase Grok AI as a versatile tool that promises to deepen user understanding, democratize information, and inject humor into digital interactions, redefining how users engage with content and comprehend complex topics."
            <|separator|>
                
                Assistant: Understood! Please provide the json input.
            """


class GrokClient:
    def __init__(self):
        self.client = xai_sdk.Client()
        self.sampler = self.client.sampler

    async def fetch_tweets(self, topic_name):
        tweets = [
            {
                "index": 1,
                "text": "Tesla will never make a concept car that doesn’t become reality",
                "url": "https://x.com/elonmusk/status/1759255283040235546",
            },
            {
                "index": 2,
                "text": "Unfortunately, very heavy Tesla obligations require that the visit to India be delayed, but I do very much look forward to visiting later this year.",
                "url": "https://x.com/elonmusk/status/1781541775183610310",
            },
            {
                "index": 3,
                "text": "Tesla Cybertruck, the finest in apocalypse defense technology!",
                "url": "https://x.com/elonmusk/status/1761962177794306542",
            },
        ]

        return tweets

    async def get_insights(self, user, topic_name, tweets):
        input_json = {"user": user, "topic": topic_name, "tweets": tweets}

        prompt = (
            PREAMBLE
            + f"<|separator|>\n\nHuman: {input_json}<|separator|>\n\nAssistant: "
        )

        print("prompt", prompt)

        insights = ""
        async for token in self.sampler.sample(
            prompt=prompt,
            max_len=1024,
            stop_tokens=["<|separator|>"],
            temperature=0.5,
            nucleus_p=0.95,
        ):
            print(token.token_str)
            insights += token.token_str
            yield token.token_str


async def main():
    grok_client = GrokClient()
    insights = await grok_client.get_insights(
        "Elon Musk",
        "Tesla",
        [
            {
                "text": "Tesla will never make a concept car that doesn’t become reality",
                "url": "https://x.com/elonmusk/status/1759255283040235546",
            },
            {
                "text": "Unfortunately, very heavy Tesla obligations require that the visit to India be delayed, but I do very much look forward to visiting later this year.",
                "url": "https://x.com/elonmusk/status/1781541775183610310",
            },
            {
                "text": "Tesla Cybertruck, the finest in apocalypse defense technology!",
                "url": "https://x.com/elonmusk/status/1761962177794306542",
            },
        ],
    )
    print("insights", insights)


if __name__ == "__main__":
    asyncio.run(main())
