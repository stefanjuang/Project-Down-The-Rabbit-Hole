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
            example output is to generate summary text of the insights. index in tweets is link with [$`{index}`] in summary
            "This feature aligns with the original meaning of 'grok' from Robert Heinlein's science fiction, which implies a profound, almost empathetic understanding of a subject. 
            Elon Musk's introduction of the 'Grok AI' via his tweets represents an intriguing advancement in how we interact with information and process understanding. 
            The concept of 'Grok, analysis!' being implemented as a feature on X (formerly Twitter) suggests that this AI tool is designed to provide deep, intuitive insights into the content posted on the platform. [1]
            The mention of 'Colon Cologne' in a humorous tweet also indicates Musk's typical blend of humor with serious technological innovations, perhaps suggesting that Grok AI could have broader applications in generating engaging and creative content that goes 'beyond' conventional boundaries. 
            More substantively, Musk's tweet about Grok AI summarizing upcoming legislation before it passes indicates a practical application aimed at transparency and public understanding of complex governmental processes. This use case highlights Grok AI's potential role in democratizing information and making intricate details more accessible to the general public. [3]
            Overall, Grok AI seems to be positioned as a tool that not only deepens understanding but does so in a way that is approachable and engaging for users. It promises to enhance user interaction with digital content by providing deeper insights and simplifying complex information, thereby enriching the user's experience and knowledge base."
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
        # print(insights)


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
