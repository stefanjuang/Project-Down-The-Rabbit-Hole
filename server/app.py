import json
import traceback
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict

from server.grok import GrokClient

from server.TwitterAPI import TwitterAPI

app = FastAPI()

grok_client = GrokClient()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust the allowed origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TopicData(BaseModel):
    topic: str

class QueryData(BaseModel):
    query: str

class AnalyzeData(BaseModel):
    user: str
    topic: str

@app.post("/searchUsrTweets")
async def searchUsrTweets(data: QueryData): 
    query = data.query
    print("In the searchUsrTweets function, query is:", query)
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is missing")

    twitter_api = TwitterAPI("Enter_Your_Bearer_Token_Here")
    
    tweets = twitter_api.fetch_tweets("from:" + query + " -is:reply")  

    if tweets:
        response_content = {"tweets": tweets}
        return JSONResponse(status_code=200, content=response_content)
    else:
        response_content = {"message": "No tweets found"}
        return JSONResponse(status_code=404, content=response_content)

@app.post("/fetch_tweets_from_topic")
async def fetch_tweets_from_topic(data: TopicData):
    tweets = await grok_client.fetch_tweets(data.topic)

    return JSONResponse(content=tweets)


@app.post("/analyze_topic")
async def analyze_topic(data: AnalyzeData):
    tweets = await grok_client.fetch_tweets(data.topic)

    try:
        stream = grok_client.get_insights(data.user, data.topic, tweets)

        async def generator():
            async for insight_chunk in stream:
                print(insight_chunk)
                yield insight_chunk

        return StreamingResponse(generator(), media_type="text/event-stream")
    except Exception as e:
        print(f"error occurred: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"message": "An error occurred"})

