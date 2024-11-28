import spacy
import yaml
import requests
import os
from dotenv import load_dotenv
from spacy.cli import download  # Import for downloading spaCy models if not installed

# Load environment variables from .env file
load_dotenv()

class APITool:
    def __init__(self):
        # Check if the model is already installed
        try:
            print("Model 'en_core_web_sm' is already loaded!")
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If not, download the model
            print("Model 'en_core_web_sm' not found. Downloading now...")
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Load Swagger specification from the local YAML file
        with open("swagger_specs/weather.yaml", "r") as file:
            self.swagger_spec = yaml.safe_load(file)
            self.base_url = self.swagger_spec['servers'][0]['url']  # Extract base URL

        # Load the API key from environment variables
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            print("Error: API key is not set in the .env file")
            exit(1)

    def extract_intent(self, user_message):
        """
        Use keyword matching to extract the intent from the user's message.
        If the intent is to ask for weather, we return 'weather'.
        """
        weather_keywords = ["weather", "forecast", "temperature", "current", "climate"]
      
        #check for weather-related keywords in the entire message
        for keyword in weather_keywords:
            if keyword in user_message.lower():
                print("intent extracted using keyword matching")
                return "weather"
        
        return None
    
    def get_api_endpoint(self, intent):
        """
        Extract the API endpoint from Swagger JSON based on the user's intent.
        For simplicity, we assume 'weather' intent will be matched with the '/v1/current' endpoint.
        """
        if intent == "weather":
            # Extract weather-related API path from Swagger documentation
            for path, details in self.swagger_spec['paths'].items():
                if "get" in details:
                    # if "weather" in details['summary'].lower():
                    return path, details['get']
        return None, None
    
    def get_parameters(self, endpoint_details, user_message):
        """
        Extract the parameters required for the API request from the Swagger documentation.
        Attempts to fill in parameters automatically from user input and .env file.
        """
        doc = self.nlp(user_message.lower())
        parameters = {}

        if "parameters" in endpoint_details:
            for param in endpoint_details["parameters"]:
                param_name = param["name"]
                param_in = param["in"]

                # First priority: auto-fill from environment variables or user message
                if param_name == "key" and self.api_key:  # For the API key
                    parameters[param_name] = self.api_key
                elif param_name == "q":  # For location
                    location = next((ent.text for ent in doc.ents if ent.label_ == "GPE"), None)
                    if location:
                        print(f"location detected: {location}")
                        parameters[param_name] = location
                    else:
                        value = input(f"Please provide the value for {param_name} ({param_in}): ")
                        parameters[param_name] = value    

        return parameters
    def make_api_request(self, endpoint, parameters):
        """
        Make an API request to the weather API using the endpoint and parameters extracted.
        """
        url = f"{self.base_url}{endpoint}"

        # Add the API key to the parameters
        parameters["key"] = self.api_key

        response = requests.get(url, params=parameters)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not fetch weather data."}

    def format_weather_response(self, weather_data):
        """
        Format the JSON weather data into a natural language message.
        """
        if "location" in weather_data and "current" in weather_data:
            location = weather_data["location"]["name"]
            region = weather_data["location"]["region"]
            country = weather_data["location"]["country"]
            temp_c = weather_data["current"]["temp_c"]
            condition = weather_data["current"]["condition"]["text"]
            humidity = weather_data["current"]["humidity"]
            wind_kph = weather_data["current"]["wind_kph"]

            return (
                f"The current weather in {location}, {region}, {country} is {temp_c}°C with {condition} condition. "
                f"Humidity is at {humidity}% and wind speed is {wind_kph} kph."
            )
        else:
            return "Sorry, I couldn't retrieve weather information at the moment."

    def process_request(self, user_message):
        """
        Process the user's message, extract intent, query API, and return response.
        """
        intent = self.extract_intent(user_message)
        
        if intent == "weather":
            # Get the appropriate API endpoint and details
            endpoint, endpoint_details = self.get_api_endpoint(intent)
            
            if endpoint:
                # Get the required parameters from the user
                parameters = self.get_parameters(endpoint_details, user_message)
                
                # Make the API request and get the data
                weather_data = self.make_api_request(endpoint, parameters)
                
                if "error" in weather_data:
                    print("Error: Could not fetch weather data.")
                else:
                    natural_language_response = self.format_weather_response(weather_data)
                    print(natural_language_response)
            else:
                print("Sorry, I couldn't find a weather API to process this request.")
        else:
            print("Sorry, I couldn't understand your request.")
            
        return "continue"    

if __name__ == "__main__":
    api_tool = APITool()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        api_tool.process_request(user_input)
