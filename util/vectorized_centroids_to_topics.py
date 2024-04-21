# This program provides an end-to-end solution for analyzing tweet vectors to determine the main topics being discussed.
# The process includes several key components:
#
# 1. KMeans Clustering: The function begins by applying the KMeans clustering algorithm to group tweet vectors into clusters.
#    This helps in identifying distinct groups or topics in the data based on vector similarity.
#
# 2. Finding Closest Points: For each cluster centroid determined by KMeans, the function identifies the closest tweet vector.
#    These vectors are considered representative of their respective clusters.
#
# 3. Summarizing Texts: Using the BART large model from the Hugging Face transformers library, the function then summarizes the tweets
#    corresponding to these closest vectors. Summarization aims to condense the tweets into their essential messages, making it easier
#    to extract meaningful topics.
#
# 4. Extracting Topics: Subsequently, the T5 model is employed to further analyze the summaries and extract keywords or phrases.
#    These serve as the topics for each cluster, representing the primary focus or subject matter of the grouped tweets.
#
# 5. Cleaning and Deduplication: Before finalizing the output, the topics undergo a cleaning process where commas are removed,
#    texts are converted to lowercase, and duplicate words are eliminated. This step ensures the clarity and uniqueness of each topic.
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import wordnet
from sklearn.cluster import KMeans
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    T5ForConditionalGeneration,
    T5Tokenizer,
)
from vectorize_tweets import vectorize_tweets

# Download WordNet data
nltk.download("words")


# Function to remove @mentions
def remove_mentions(tweet):
    # Regex to find mentions and handle spaces and punctuation
    cleaned_tweet = re.sub(r"\s*@\w+\s*", " ", tweet)
    # Remove additional spaces created by replacements
    cleaned_tweet = re.sub(r"\s+", " ", cleaned_tweet).strip()
    return cleaned_tweet


def is_word_in_wordnet(word):
    """Check if a word is in WordNet"""
    return bool(wordnet.synsets(word))


def filter_using_wordnet(tweets):
    filtered_tweets = []
    for tweet in tweets:
        words_in_tweet = tweet.split()
        valid_words = [word for word in words_in_tweet if is_word_in_wordnet(word)]
        if valid_words:
            filtered_tweets.append(" ".join(valid_words))
    return filtered_tweets


def find_closest_points(data, centroids):
    closest_indices = []
    for centroid in centroids:
        distances = np.linalg.norm(data - centroid, axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)
    return closest_indices


def summarize_texts(texts):
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    summaries = []
    for text in texts:
        input_ids = tokenizer(text, return_tensors="pt", truncation=True).input_ids
        output = model.generate(input_ids, no_repeat_ngram_size=3, num_beams=4)
        predicted = tokenizer.decode(output[0], skip_special_tokens=True)
        summaries.append(predicted)
    return summaries


def extract_topics(summaries):
    tokenizer = T5Tokenizer.from_pretrained("Voicelab/vlt5-base-keywords")
    model = T5ForConditionalGeneration.from_pretrained("Voicelab/vlt5-base-keywords")
    topics = []
    task_prefix = "Keywords: "
    for summary in summaries:
        input_sequences = task_prefix + summary
        input_ids = tokenizer(
            input_sequences, return_tensors="pt", truncation=True
        ).input_ids
        output = model.generate(input_ids, no_repeat_ngram_size=3, num_beams=4)
        predicted = tokenizer.decode(output[0], skip_special_tokens=True)
        topics.append(predicted)
    return topics


def clean_and_deduplicate(entry):
    entry = entry.replace(",", "").lower()
    words = entry.split()
    unique_words = list(set(words))
    return " ".join(unique_words)


def analyze_tweet_vectors(tweet_vectors, tweets_list):
    kmeans = KMeans(n_clusters=20, random_state=42)
    kmeans.fit(tweet_vectors)
    centroids = kmeans.cluster_centers_

    closest_indices = find_closest_points(tweet_vectors, centroids)
    closest_tweets = [tweets_list[i] for i in closest_indices]
    cleaned_tweets = [remove_mentions(tweet) for tweet in closest_tweets]
    summaries = summarize_texts(cleaned_tweets)
    topics = extract_topics(summaries)

    # Clean and deduplicate topics before returning
    cleaned_topics = [clean_and_deduplicate(topic) for topic in topics]
    # Filter using WordNet
    filtered_tweets_wordnet = filter_using_wordnet(cleaned_topics)
    return filtered_tweets_wordnet


# Example usage:
# Assuming 'tweet_vectors' and 'tweets_list_new' are provided

file_path_new = "./util/elonmusk.csv"
data = pd.read_csv(file_path_new)
tweets = data["Tweets"].tolist()
tweet_vectors = vectorize_tweets(tweets)
topics = analyze_tweet_vectors(tweet_vectors, tweets)
print(topics)
