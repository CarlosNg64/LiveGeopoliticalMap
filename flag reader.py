import re

def extract_special_characters(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to match individual emojis or special symbols and two-character sequences
    pattern = r'[\U0001F000-\U0001FFFF]{1,2}'

    # Find all matching sequences
    special_characters = re.findall(pattern, content)
    
    return special_characters

# File path to the text document (use raw string to avoid unicode escape error)
file_path = r'c:\Users\oneto\Documents\GitHub\LiveGeopoliticalMap\telegram_chat.txt'

# Extract special characters and two-character sequences
special_characters = extract_special_characters(file_path)

# Print the extracted elements
for element in special_characters:
    print(element)
