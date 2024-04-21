import requests

class TwitterAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.endpoint_url = "https://api.twitter.com/2/tweets/search/all"
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def make_request(self, params):
        try:
            response = requests.get(self.endpoint_url, headers=self.headers, params=params)
            response.raise_for_status()  
            return response.json()  
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
            return None

    def fetch_tweets(self, query):
        query_params = {"query": query, "expansions": "author_id", "max_results": 500}
        all_tweets = []
        counter = 1

        response_data = self.make_request(query_params)

        if response_data is not None:
            all_tweets.extend(response_data.get("data", []))
            next_token = response_data.get("meta", {}).get("oldest_id")

            while next_token and counter < 20:
                query_params["until_id"] = next_token
                response_data = self.make_request(query_params)
                counter += 1
                if response_data is not None:
                    all_tweets.extend(response_data.get("data", []))
                    next_token = response_data.get("meta", {}).get("oldest_id")
                else:
                    break

            return all_tweets
        else:
            print("Failed to fetch data from the endpoint.")
            return []


if __name__ == "__main__":
    access_token = "lalalala"  
    twitter_api = TwitterAPI(access_token)
    query = "from:elonmusk -is:reply"
    tweets = twitter_api.fetch_tweets(query)
    for tweet in tweets:
        print("Tweet ID:", tweet.get("id"))
        print("Author ID:", tweet.get("author_id"))
        print("Text:", tweet.get("text"))
        print("--------------------------------------------")
    print("Total number of tweets:", len(tweets))
