'''
import re
import random

# Clean Gutenberg text to remove headers and footers
def clean_gutenberg_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    
    if start_match and end_match:
        clean_text = text[start_match.end():end_match.start()].strip()
    else:
        clean_text = text
    
    return clean_text

# Replace specific words in the text
def find_and_replace(text, replacements):
    for old_word, new_word in replacements.items():
        text = re.sub(rf'\b{old_word}\b', new_word, text, flags=re.IGNORECASE)
    return text

# Erasure method: Remove all occurrences of a specific letter
def erasure_lipogram(text, letter_to_remove):
    return text.replace(letter_to_remove, '')

# Generate a combined cento from multiple texts
def generate_cento(cleaned_texts, num_sentences=20):
    sentences = []
    for text in cleaned_texts:
        split_text = re.split(r'(?<=[.!?])\s+', text)
        sampled_sentences = random.sample(split_text, min(len(split_text), num_sentences // len(cleaned_texts)))
        sentences.extend(sampled_sentences)
    random.shuffle(sentences)
    return " ".join(sentences)

# Convert the text to HTML structure
def text_to_html(text):
    html_content = """
    <html>
    <head>
        <title>Combined Story</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            h1 { text-align: center; color: #333; }
            p { line-height: 1.6; color: #555; }
        </style>
    </head>
    <body>
        <h1>Combined Story</h1>
        <p>A blend of the classic stories: <br>
             ♡ Dracula (published 1897) by Bram Stoker ♡<br>
             ♡ Strange Case of Dr Jekyll and Mr Hyde (published 1886) by Robert Louis Stevenson ♡<br>
             ♡ Frankenstein (published 1818) by Mary Shelley ♡<br>
             ♡ Carmilla (published 1872) by Sheridan Le Fanu ♡<br>
             ♡ Grimm's Fairy Tales (published 1812) by Jacob Grimm and Wilhelm Grimm ♡
        </p>        
        <p>{}</p>
    </body>
    </html>
    """.replace("{}", text.replace("\n", "<br>"))
    return html_content
    

# Main execution block
if __name__ == "__main__":
    # File paths for the texts
    file_paths = ["frank.txt", "carmilla.txt", "drac.txt", "jekyllhyde.txt", "grimm.txt"]
    cleaned_texts = [clean_gutenberg_text(path) for path in file_paths]
    
    # Apply Find and Replace method
    replacements = {"vampire": "ghost", "monster": "shadow", "doctor": "sorcerer"}
    cleaned_texts = [find_and_replace(text, replacements) for text in cleaned_texts]
    
    # Apply Erasure/Lipogram method (remove word 'him')
    cleaned_texts = [erasure_lipogram(text, 'him') for text in cleaned_texts]
    
    # Generate Cento
    cento_story = generate_cento(cleaned_texts, num_sentences=30)
    
    # Convert the combined text to HTML
    html_story = text_to_html(cento_story)
    
    # Write to an HTML file
    with open("combined_story.html", "w", encoding="utf-8") as file:
        file.write(html_story)
    
    print("Combined story generated. Open combined_story.html to view it.")
'''
'''
import re
import json
import string
from collections import Counter

# Clean Gutenberg text to remove headers and footers
def clean_gutenberg_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    
    if start_match and end_match:
        clean_text = text[start_match.end():end_match.start()].strip()
    else:
        clean_text = text
    
    return clean_text

# Tokenize text into words
def tokenize(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    words = text.split()  # Split into words
    return words

# Process all texts and create a bag of words
def create_bag_of_words(file_paths):
    word_counts = Counter()
    
    for file_path in file_paths:
        cleaned_text = clean_gutenberg_text(file_path)
        words = tokenize(cleaned_text)
        word_counts.update(words)
    
    return dict(word_counts)

# Main execution block
if __name__ == "__main__":
    # File paths for the texts
    file_paths = ["frank.txt", "carmilla.txt", "drac.txt", "jekyllhyde.txt", "grimm.txt"]
    
    # Create bag of words
    bag_of_words = create_bag_of_words(file_paths)
    
    # Save to a JSON file
    with open("bag_of_words.json", "w", encoding="utf-8") as json_file:
        json.dump(bag_of_words, json_file, ensure_ascii=False, indent=4)
    
    print("Bag of words JSON file generated: bag_of_words.json")
'''
'''
import json
import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
nltk.data.path.append("/Users/zubeyda/nltk_data")

# Download WordNet data (if you haven't already)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load bag of words from JSON
def load_bag_of_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Get the most relevant synset (category) for a word
def get_main_synset(word):
    synsets = wn.synsets(word)
    if synsets:
        return synsets[0].lexname()  # Get the main category of the first synset
    return "uncategorized"

# Categorize words based on their WordNet synsets
def categorize_words(bag_of_words):
    categorized_words = defaultdict(list)
    
    for word in bag_of_words.keys():
        category = get_main_synset(word)
        categorized_words[category].append(word)
    
    return dict(categorized_words)

# Main execution block
if __name__ == "__main__":
    # Load bag of words
    bag_of_words = load_bag_of_words("bag_of_words.json")

    # Categorize words using WordNet
    categorized_words = categorize_words(bag_of_words)

    # Save to a new JSON file
    with open("categorized_words.json", "w", encoding="utf-8") as json_file:
        json.dump(categorized_words, json_file, ensure_ascii=False, indent=4)
    
    print("Categorized words saved to categorized_words.json")
'''

import json
import nltk
from nltk.corpus import wordnet as wn

# Load categorized words from JSON
def load_categorized_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Filter out categories with fewer than 10 words
def filter_categories(categorized_words, min_count=10):
    return {category: words for category, words in categorized_words.items() if len(words) >= min_count}

# Extract the categories (keys) from the filtered categorized words
def get_categories(categorized_words):
    return list(categorized_words.keys())

# Main execution block
if __name__ == "__main__":
    # Load categorized words
    categorized_words = load_categorized_words("categorized_words.json")

    # Filter categories with at least 10 words
    filtered_words = filter_categories(categorized_words, min_count=10)

    # Get the list of categories
    categories = get_categories(categorized_words)
    
    
    # Define the origin rule for Tracery grammar
    origin_rule = [
        "In the year #noun.time#, #noun.person# embarked on a mission to explore #noun.location#.",
        "The #noun.animal# was discovered in the #noun.location#, a strange creature with #noun.attribute# eyes.",
        "As the #noun.group# of explorers ventured through the #noun.location#, they encountered a mysterious #noun.artifact# that seemed to #verb.cognition# their minds.",
        "At the moment, the spaceship's #noun.artifact# began to malfunction, and the crew felt an overwhelming sense of #noun.feeling#.",
        "They had no choice but to #verb.communication# for help, hoping the signal would reach the nearest #noun.group# of #noun.person# at #noun.location#.",
        "Suddenly, a #noun.phenomenon# occurred, altering the fabric of time and space. The #noun.location# began to #verb.change#, its shape and structure becoming unrecognizable.",
        "In the midst of the chaos, a #noun.person# suddenly began to #verb.cognition# the existence of a parallel universe, where #noun.state# ruled instead of #noun.time#.",
        "The explorers decided to #verb.motion# to the #noun.location#, determined to uncover the secrets hidden within.",
        "The #noun.event# they faced was unlike any other, as the laws of physics seemed to #verb.change#, and the very #noun.motive# of the mission was called into question.",
        "With every passing moment, the #noun.group# began to lose all sense of #noun.cognition#, as their minds were overtaken by the strange force emanating from the #noun.artifact#."
    ]

    # Prepare the final JSON structure with the origin rule and the filtered categories
    final_json = {
        "origin": origin_rule,
        "categories": filtered_words
    }

    # Output the categories
    print(categories)

    # Save to a new JSON file
    with open("filtered_categorized_words.json", "w", encoding="utf-8") as json_file:
        json.dump(final_json, json_file, ensure_ascii=False, indent=4)

    print("Filtered categorized words and origin rule saved to filtered_categorized_words.json")
