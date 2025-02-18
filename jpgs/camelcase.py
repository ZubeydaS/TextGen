"""
import json

# Load categorized words from JSON file
with open('filtered_categorized_words.json', 'r') as f:
    categories = json.load(f)

# Function to convert category name from word.word format to CamelCase
def to_camel_case(text):
    # Split by the dot and capitalize each part, but keep the first part lowercase
    parts = text.split('.')
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])

# Convert category names to CamelCase, leaving words unchanged
converted_categories = {}

for category, words in categories.items():
    # Convert category names (keys) to CamelCase
    camel_case_category = to_camel_case(category)
    
    # Keep the words inside the category unchanged
    converted_categories[camel_case_category] = words

# Save the updated categories back to JSON
with open('grammar.json', 'w') as f:
    json.dump(converted_categories, f, indent=4)

# Print the updated category names
print("Updated Categories:")
for category in converted_categories.keys():
    print(category)
"""
import json
import re

# Load categorized words from JSON file
with open('filtered_categorized_words.json', 'r') as f:
    categories = json.load(f)

# Function to convert word.word format to CamelCase
def to_camel_case(text):
    parts = text.split('.')
    return ''.join(word.capitalize() for word in parts)

# Convert both category names and words inside categories to CamelCase
converted_categories = {}

for category, words in categories.items():
    # Convert category names to CamelCase
    camel_case_category = to_camel_case(category)
    
    # Convert each word inside the category to CamelCase
    camel_case_words = [to_camel_case(word) if isinstance(word, str) else word for word in words]
    
    converted_categories[camel_case_category] = camel_case_words

# Save the updated categories back to JSON
with open('grammar.json', 'w') as f:
    json.dump(converted_categories, f, indent=4)

# Print the updated category names
print("Updated Categories:")
for category in converted_categories.keys():
    print(category)
