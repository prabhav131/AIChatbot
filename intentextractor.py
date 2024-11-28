import re
from langchain_ollama import OllamaLLM
import spacy
from spacy.cli import download

# Check if the model is already installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not, download the model
    print("Model 'en_core_web_sm' not found. Downloading now...")
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# # Now you can use `nlp` as usual
# doc = nlp("Steve's Apple is opening a new office in New York on January 15.")

# for ent in doc.ents:
#     print(ent.text, ent.label_)

class UnifiedExtractor:
    def __init__(self):
        # Initialize LLM for more complex parsing
        self.llm = OllamaLLM(model="tinydolphin")
        
    def extract_intent(self, user_message):
        # Simple intent extraction logic (this could be enhanced)
        if "email" in user_message or "send" in user_message:
            return "SEND_EMAIL"
        elif "weather" in user_message or "hot" in user_message or "cold" in user_message:
            return "WEATHER_CHECK"
        else:
            return "UNKNOWN"

    def extract_metadata(self, user_message, intent):
        doc = nlp(user_message)
        metadata = {}
        
        if intent == "SEND_EMAIL":
            # Extract recipient's name (Assume the format "to {name}")
            recipient = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
            metadata['recipient'] = recipient
            
            # Ask for email address if not provided
            if not re.search(r'[\w\.-]+@[\w\.-]+', user_message):
                metadata['email'] = input(f"Please provide {recipient}'s email address: ")
            
            # Extract or ask for subject and body
            metadata['subject'] = input("What should the email subject be? ")
            metadata['body'] = input("What should the email body be? ")

        elif intent == "WEATHER_CHECK":
            # Extract location
            location = next((ent.text for ent in doc.ents if ent.label_ == "GPE"), None)
            metadata['location'] = location if location else input("Please provide a location for the weather check: ")

        return metadata

    def process_request(self, user_message):
        intent = self.extract_intent(user_message)
        metadata = self.extract_metadata(user_message, intent)
        
        if intent == "SEND_EMAIL":
            # Call the email tool with the extracted metadata
            EmailTool().send_email(metadata)
        elif intent == "WEATHER_CHECK":
            # Call the API tool for weather data
            APITool().get_weather(metadata)
        else:
            print("Sorry, I didn't understand the request.")

class EmailTool:
    def send_email(self, metadata):
        print(f"Sending email to {metadata['recipient']} at {metadata['email']}")
        print(f"Subject: {metadata['subject']}")
        print(f"Body: {metadata['body']}")

class APITool:
    def get_weather(self, metadata):
        print(f"Checking weather for {metadata['location']}")

# Example usage
user_message = input("Enter your message: ")
UnifiedExtractor().process_request(user_message)
