import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import spacy
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from spacy.cli import download  # Import for downloading spaCy models if not installed

# Load environment variables
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL = os.getenv("EMAIL_USER")
SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")

class EmailTool:
    def __init__(self):
        # Load the "tinydolphin" model
        self.model = OllamaLLM(model="orca-mini")
        
        # Check if the model is already installed
        try:
            print("Model 'en_core_web_sm' is already loaded!")
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If not, download the model
            print("Model 'en_core_web_sm' not found. Downloading now...")
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            
        self.recipient_name = None    

    def extract_intent(self, user_message):
        """
        Detect if the user's intent is to send an email based on keywords.
        """
        user_message = user_message.lower()
        
        if "email" in user_message or "send" in user_message or "message" in user_message:
            return "send_email"
        
        return None

    def extract_name(self, user_message):
        """
        Use spaCy NER to extract the recipient's name from the user's message.
        """
        doc = self.nlp(user_message)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def get_user_input(self):
        """
        Prompt the user for recipient email and message, using NER to find the name.
        """
        # Get user input for the message
        user_message = input("What would you like to say in the email? ")
        
        if self.recipient_name:
            recipient_email = input(f"Please provide {self.recipient_name}'s email address: ")
        else:
            recipient_email = input("Please provide the recipient's email address: ")
            self.recipient_name = input("Please provide recipient's name: ")
        
        return recipient_email, user_message

    def craft_email(self, recipient_email, user_message):
        """
        Uses LLM to craft an email subject and body based on the recipient's email and user's message.
        """
        prompt = f"""
Create a short friendly email addressed to {self.recipient_name} based on the message: "{user_message}". 
Provide only the subject and body of the email in the following format:

Subject: [Insert subject here, relevant to the user message]
Body: [Insert body here, polite and concise]
Sign off at the end under my name- {os.getenv("USER_NAME")}

Do not include any additional text, instructions, or clarifications. The email should be polite and clear, fitting the message context.
        """

        # Pass the prompt as a list to `generate`
        response = self.model.invoke(prompt)

        subject, body = "", ""
        lines = response.splitlines()

        for line in lines:
            line = line.strip()
            if line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.lower().startswith("body:") or subject:
                body += line + "\n"

        return subject.strip(), body.strip()

    def confirm_and_send_email(self, recipient_email, subject, body):
        """
        Confirm with the user and send the email using SMTP.
        """
        print("\nPlease review the email details:")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        
        confirm = input("Do you want to send this email? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                # Setup email message
                msg = EmailMessage()
                msg["From"] = SMTP_EMAIL
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.set_content(body)
                
                # Send email using SMTP
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                    smtp.starttls()
                    smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
                    smtp.send_message(msg)
                
                print("Email sent successfully!")
            except Exception as e:
                print("Failed to send email:", str(e))
        else:
            print("Email sending cancelled.")

    def handle_email_conversation(self):
        """
        Main method to handle the email conversation and process the email request.
        """
        print("Let's get started with sending an email!")
        recipient_email, user_message = self.get_user_input()
        subject, body = self.craft_email(recipient_email, user_message)
        self.confirm_and_send_email(recipient_email, subject, body)

    def handle_email_conversation_with_initial_message(self, first_message):
        """
        Main method to handle the email conversation and process the email request.
        """
        print("Let's get started with sending an email!")
        recipient_name = self.extract_name(first_message)
        if recipient_name:
            recipient_email = input(f"Please provide {recipient_name}'s email address: ")
        else:
            recipient_email = input("Please provide the recipient's email address: ")
            recipient_name = input("Please provide recipient's name: ")
            
        user_message = first_message
        subject, body = self.craft_email(recipient_email, user_message)
        self.confirm_and_send_email(recipient_email, subject, body)
        
        return "continue"

# Example usage of the EmailTool
if __name__ == "__main__":
    email_tool = EmailTool()
    user_input = input("You: ")
    email_tool.recipient_name = email_tool.extract_name(user_input)
    
    # Check for email intent
    if email_tool.extract_intent(user_input) == "send_email":
        email_tool.handle_email_conversation()
    else:
        print("No email intent detected.")
