# pip install tweepy

import tweepy

# Replace the following strings with your own keys and tokens
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

try:
    # Get the authenticated user's details
    user = api.verify_credentials()
    if user:
        print('Authentication successful.')
        print('Username:', user.screen_name)
    else:
        print('Failed to authenticate.')
except Exception as e:
    print('Error during authentication:', e)

