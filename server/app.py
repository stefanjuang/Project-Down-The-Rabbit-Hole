import asyncio

import requests  # if you need to make external API calls to Grok
from flask import Flask, jsonify, request

from server.grok import GrokClient

app = Flask(__name__)


@app.route("/analyze_topic", methods=["POST"])
def analyze_topic():
    grok_client = GrokClient()
    data = request.json
    topic_name = data["topic"]
    tweets = data["tweets"]

    # Here, call the Grok API to process the input and generate insights.
    insights = asyncio.run(grok_client.get_insights(topic_name, tweets))

    return jsonify(insights)


if __name__ == "__main__":
    app.run(debug=True)
