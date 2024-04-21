import requests

def make_request(endpoint, headers=None, params=None):
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None

endpoint_url = "https://api.twitter.com/2/tweets/search/all"


access_token = "lalalala" # put your bearer token here


query_params = {"query": "from:elonmusk -is:reply", "expansions": "author_id", "max_results": 500}


headers = {"Authorization": f"Bearer {access_token}"}


response_data = make_request(endpoint_url, headers=headers, params=query_params)
all_tweets = []

counter = 1

if response_data is not None:
    all_tweets.extend(response_data.get("data", []))
    next_token = response_data.get("meta", {}).get("oldest_id")

    
    while next_token and counter < 20:
        query_params["until_id"] = next_token
        response_data = make_request(endpoint_url, headers=headers, params=query_params)
        counter += 1
        if response_data is not None:
            all_tweets.extend(response_data.get("data", []))
            next_token = response_data.get("meta", {}).get("oldest_id")
        else:
            break

    
    for tweet in all_tweets:
        print("Tweet ID:", tweet.get("id"))
        print("Author ID:", tweet.get("author_id"))
        print("Text:", tweet.get("text"))
        print("--------------------------------------------")

    print("Total number of tweets:", len(all_tweets))
else:
    print("Failed to fetch data from the endpoint.")

