# Requirement:
# pip install deep-translator
# pip install requests


import requests
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator

# ANSI color codes for colorful output
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
RESET = '\033[0m'

# AnkiConnect API URL
API_URL = "http://localhost:8765"

# Get user input for deck name and URL
deck_name = input("Enter deck name to add words: "+ MAGENTA)
urll = input(RESET + "Enter URL to add words: "+ MAGENTA)

# Parse URL to extract query parameters
word_list = []
word = ""
# extract words from url
parsed_url = urlparse(urll)
query_params = parse_qs(parsed_url.query)
# reads str and extracts words and sentences and adds them to the list
if 'text' in query_params:
    encoded_text = query_params['text'][0]
    # To add the last word, add \n to end of encoded_text
    encoded_text += "\n"
    for text in encoded_text:
        if text == "\n":
          word_list.append(word)
          word = ""
        else :
          word += text
else:
    print("No 'text' parameter found in the URL.")

def get_meanings(word):
    translated = GoogleTranslator(source='auto', target='fa').translate(word)
    return translated

# Main execution
if __name__ == "__main__":
    checkpoint = []
    for word in word_list:
        # get meaning of word
        meaning = get_meanings(word)
        if meaning:
            # AnkiConnect action to add a note
            add_note_action = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": deck_name,
                        "modelName": "Basic",  # Change if needed
                        "fields": {
                            "Front": word,
                            "Back": meaning
                        }
                    }
                }
            }
            response = requests.post(API_URL, json=add_note_action)

            # Check Anki response
            if response.status_code == 200:
                checkpoint.append(True)
                print(f"{YELLOW} {word} {GREEN} added successfully! {RESET}")
            else:
                checkpoint.append(False)
                print(f"{YELLOW}{word} {RED}Failed to add. {RESET}")
        else:
            print(RED + "No meaning found." + RESET)

    # Check all words add to Anki
    if all(checkpoint):
        print(f"{GREEN} All words added successfully {RESET}")

    input("Press Enter to exit...")
