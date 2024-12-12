import csv
import tiktoken

# Load the CSV file
csv_file = 'datasets/merged.csv'

# Initialize the tokenizer (for GPT models, using tiktoken)
encoder = tiktoken.get_encoding("cl100k_base")

# Read the CSV file and concatenate all text data
all_text = ""
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        # Concatenate each row's text data (adjust based on your CSV structure)
        all_text += ' '.join(row) + "\n"  # Space between columns, newline after each row

# Tokenize the concatenated text
tokens = encoder.encode(all_text)

# Get the number of tokens
token_length = len(tokens)

print(f"Token length of the CSV file: {token_length}")