import pandas as pd
import ast

# Load CSV containing ASL data
df = pd.read_csv('./data/how2sign_val_asl.csv', delimiter="\t")

def safe_parse_list(asl_tokens_str):
    """Safely parses ASL_TOKENS from a string to a list."""
    try:
        return ast.literal_eval(asl_tokens_str)  # Convert to list safely
    except (ValueError, SyntaxError):
        return []  # Return empty list if parsing fails

def match_sentence_to_video(input_sentence, top_n=3):
    """
    Matches words in the input sentence to ASL_TOKENS and returns the videos 
    with the highest word match frequency.
    """
    input_words = set(input_sentence.lower().split())  # Convert input to a set of words

    matches = []

    for _, row in df.iterrows():
        asl_tokens = safe_parse_list(row['ASL_TOKENS'])  # Convert ASL_TOKENS to a list
        if not isinstance(asl_tokens, list):  
            continue  # Skip rows where parsing failed

        asl_token_set = set(map(str.lower, asl_tokens))  # Convert to lowercase set
        common_words = input_words.intersection(asl_token_set)  # Find matching words
        match_score = len(common_words)  # Score based on word frequency match

        if match_score > 0:  # Only store relevant matches
            matches.append((row['SENTENCE_NAME'], match_score))

    # Sort by highest word match count
    matches.sort(key=lambda x: x[1], reverse=True)

    # Return the top N matches
    return [match[0] for match in matches[:top_n]] if matches else None

# Example Usage
input_sentence = "it's not segmented like that"
matched_videos = match_sentence_to_video(input_sentence)
print("Best Matched Videos:", matched_videos)
