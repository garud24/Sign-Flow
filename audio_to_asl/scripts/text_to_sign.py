import re

# Define rules for converting text to a simplified sign language grammar
def convert_to_sign_grammar(text):
    """
    Converts English text into a simplified Sign Language grammar format.
    """
    # Common words to remove (articles, auxiliary verbs, prepositions, etc.)
    remove_words = {"is", "are", "was", "were", "am", "the", "a", "an", "to", "in", "on", "at", "of"}

    # Tokenize and filter unnecessary words
    words = text.lower().split()
    filtered_words = [word for word in words if word not in remove_words]

    # If sentence length is more than one word, rearrange (ASL often uses topic-comment structure)
    if len(filtered_words) > 1:
        filtered_words.append(filtered_words.pop(0))  # Move subject to the end
    
    # Join words and convert to uppercase for uniformity
    return " ".join(filtered_words).upper()

if __name__ == "__main__":
    sample_text = "She is going to school."
    sign_sentence = convert_to_sign_grammar(sample_text)
    print("Converted Sign Language Sentence:", sign_sentence)
