import re
import csv

def read_character_names(file_path):
    character_names = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if len(row) == 2:
                character, name = row
                character_names[character] = name
    return character_names

def read_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    messages = content.split('%%%%%%%%%%%%%%%')
    return [message.strip() for message in messages if message.strip()]

def tag_messages(messages, character_names):
    tagged_messages = []
    for message in messages:
        tags = set()
        for character, name in character_names.items():
            if character in message:
                tags.add(name)
        tagged_messages.append((message, tags))
    return tagged_messages

# File paths
character_names_file = r'c:\Users\oneto\Documents\GitHub\LiveGeopoliticalMap\flags_n_tags.csv'
text_file_path = r'c:\Users\oneto\Documents\GitHub\LiveGeopoliticalMap\telegram_chat.txt'

# Read the character names from the CSV file
character_names = read_character_names(character_names_file)

# Read and split the text file into messages
messages = read_messages(text_file_path)

# Tag each message with country names and characters
tagged_messages = tag_messages(messages, character_names)

# Print the tagged messages
for message, tags in tagged_messages:
    print(f"Message: {message}")
    print(f"Tags: {', '.join(tags)}")
    print('-' * 40)
