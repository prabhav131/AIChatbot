# Import necessary classes for integrating with Ollama and LangChain
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class GenericTool:
    def __init__(self):
        # Define the template for the assistant's response
        self.template = """
        You are an assistant. Respond to the user's message as directly and concisely as possible. 
        If you are not sure what something means in the question, always reply with "I don't understand. Could you please try again?"

        User message: {question}
        """
        
        # Initialize the model with the specified "tinydolphin" model
        self.model = OllamaLLM(model="dolphin-phi")
        # self.model = OllamaLLM(model="tinydolphin")
        # self.model = OllamaLLM(model="orca-mini")
        
        # Create a ChatPromptTemplate using the defined template
        self.prompt = ChatPromptTemplate.from_template(template=self.template)
        
        # Combine the prompt template with the model to create a processing chain
        self.chain = self.prompt | self.model
        
    def get_response(self, question):
        """
        Method to get a response from the LLM based on the provided question.
        
        Args:
            question (str): The question to be answered by the assistant.

        Returns:
            str: The response from the LLM.
        """
        # Use the model chain to generate a response based on the user's question.
        result = self.chain.invoke({"question": question})
        return result

    def handle_conversation(self):
        """
        Function to handle the user interaction with the virtual assistant.
        This function manages the input-output loop where the user can
        continuously ask questions until they type 'exit' to quit.
        """
        
        # Infinite loop for continuous conversation until the user types 'exit'.
        while True:
            # Get input from the user.
            user_input = input("You: ")
            
            # Check if the user wants to exit the conversation.
            if user_input.lower() == 'exit':
                break
            
            result = self.get_response(user_input)
            # Print the assistant's response.
            print("Generic Bot:", result)
    
    def handle_conversation_with_initial_message(self, first_message):
        """
        Function to handle the user interaction with an initial message.
        Starts with the given initial message, then continues in a loop.
        
        Parameters:
            first_message (str): The initial message to start the conversation.
        """
        
        # Process the initial message first
        user_input = first_message
        result = self.get_response(user_input)
        print("Generic Bot:", result)       
            
        return "continue"    

# Entry point for the script, ensuring that the conversation handler
# only runs when the script is executed directly, not when imported.
if __name__ == "__main__":
    assistant = GenericTool()  # Create an instance of the GenericTool
    assistant.handle_conversation()  # Start the conversation
