# pip install tweepy

import os
from os.path import dirname, join

import tweepy
import xai_sdk
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(verbose=True, dotenv_path=dotenv_path)

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

try:
    # Get the authenticated user's details
    user = api.verify_credentials()
    if user:
        print("Authentication successful.")
        print("Username:", user.screen_name)
    else:
        print("Failed to authenticate.")
except Exception as e:
    print("Error during authentication:", e)
