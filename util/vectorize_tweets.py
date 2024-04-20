# Need ~6G of RAM for 335M params model
# package version sentence-transformers==2.7.0

from sentence_transformers import SentenceTransformer

# Initialize the model globally if it doesn't need to be reloaded each time
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

def vectorize_tweets(tweets):
    """
    Vectorizes a list of tweets using a Sentence Transformer model.
    
    Args:
    tweets (list of str): A list of tweets to be vectorized.
    
    Returns:
    tuple: A tuple containing the vector representations of the tweets and a matrix of cosine similarities.
    """
    if not tweets:
        return []  # Return empty lists if the input list is empty

    # Encode the tweets
    embeddings = model.encode(tweets)

    return embeddings

# Example usage of the function
# tweets = ["Tweet about food.", "Tweet about sports.", "Another tweet about politics."]
# vectors = vectorize_tweets(tweets)
