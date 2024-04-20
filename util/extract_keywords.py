# Use a pipeline as a high-level helper
# Need ~6G of RAM for 334M params model

from transformers import T5Tokenizer, T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained("Voicelab/vlt5-base-keywords")
tokenizer = T5Tokenizer.from_pretrained("Voicelab/vlt5-base-keywords")

def extract_keywords(tweets):
    """
    Extracts keywords from a list of tweets using a T5 model specialized in keyword extraction.
    
    Args:
    tweets (list of str): A list of tweets from which to extract keywords.
    
    Returns:
    list of str: A list of keywords extracted from each tweet.
    
    Requires:
    - A substantial amount of RAM (~6G) due to the large model parameters.
    """
    if not tweets:
        return []  # Early return if the input list is empty

    task_prefix = "Keywords: "
    results = []

    for tweet in tweets:
        input_sequences = [task_prefix + tweet]
        input_ids = tokenizer(input_sequences, return_tensors="pt", truncation=True).input_ids
        
        output = model.generate(input_ids, no_repeat_ngram_size=3, num_beams=4)
        predicted_keywords = tokenizer.decode(output[0], skip_special_tokens=True)
        
        results.append(predicted_keywords)
    
    return results

# Example usage of the function

# Example input:
# tweets = [
#     "Christina Katrakis, who spoke to the BBC from Vorokhta in western Ukraine, relays the account of one family, who say Russian soldiers shot at their vehicles while they were leaving their village near Chernobyl in northern Ukraine. She says the cars had white flags and signs saying they were carrying children.",
#     "Decays the learning rate of each parameter group by gamma every step_size epochs. Notice that such decay can happen simultaneously with other changes to the learning rate from outside this scheduler. When last_epoch=-1, sets initial lr as lr.",
#     "Hello, I'd like to order a pizza with salami topping.",
# ]

# return output:
# ['Christina Katrakis, Ukraine, Russian soldiers',
#  'gamma every step-size epochs, learning rate',
#  'pizza, salami topping']


