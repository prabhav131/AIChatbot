# Import the necessary tools
from apitool import APITool
from emailtool import EmailTool
from ragtool import RAGTool
from generictool import GenericTool
from schedulemeeting import MeetingTool

class Chatbot:
    def __init__(self):
        print("initialising generic tool...")
        self.generictool = GenericTool()
        print("initialising RAG tool...")
        self.ragtool = RAGTool()
        print("initialising email tool...")
        self.emailtool = EmailTool()
        print("initialising meeting tool...")
        self.schedule_meeting_tool = MeetingTool()
        print("initialising API tool...")
        self.apitool = APITool()

    def extract_intent(self, user_message):
        """
        Detect the user's intent based on keywords for different tools.
        """
        if "meeting" in user_message or "schedule" in user_message:
            return "schedule_meeting"
        if "email" in user_message or "send" in user_message:
            return "send_email"
        if "weather" in user_message:
            return "call_api"
        if "document" in user_message or "search" in user_message:
            return "search_rag"
        return "generic"

    def handle_conversation(self, user_message):
        """
        Main conversation handler that routes to the correct tool based on intent.
        """
        
        # Extract user intent
        intent = self.extract_intent(user_message)
        
        if intent == "send_email":
            # Pass the user message to the email tool
            print("routing to email bot...")
            result = self.emailtool.handle_email_conversation_with_initial_message(user_message)
        
        elif intent == "search_rag":
            # Pass the user message to the RAG tool
            print("routing to rag bot...")
            result = self.ragtool.handle_rag_conversation()
        
        elif intent == "schedule_meeting":
            # Pass the user message to the schedule meeting tool
            print("routing to scheduler bot...")
            result = self.schedule_meeting_tool.schedule(user_message)
        
        elif intent == "call_api":
            # Call the API tool method
            print("routing to api bot...")
            result = self.apitool.process_request(user_message)
        
        else:
            # Use generic tool if no specific intent is detected
            print("routing to generic bot...")
            result = self.generictool.handle_conversation_with_initial_message(user_message)
            
        # After each tool completes its action, continue the conversation
        if result == "continue":
            return "continue"

        return "exit"  # Optionally, exit if not handled correctly        


if __name__ == "__main__":
    chatbot = Chatbot()
    # Print a welcome message to the user.
    print("Welcome to the Virtual Assistant! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        # Check if the user wants to exit the conversation
        if user_input.lower() == 'exit':
            break
            
        result = chatbot.handle_conversation(user_input)
        if result == "exit":
            break
