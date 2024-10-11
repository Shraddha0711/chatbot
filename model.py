from anthropic import AnthropicVertex
import json
from google.oauth2 import service_account
import vertexai
import os
from prompt import Prompt
from dotenv import load_dotenv
load_dotenv()

LOCATION="us-central1" # or "us-east5"

credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
with open(credentials_path, 'r') as file:
    key_dict = json.load(file)

access_token_path=os.getenv("access_token")
with open(access_token_path, 'r') as file:
    access_token = json.load(file)




location="us-east5"
project_id="886891114006"
# print(key_dict)
# credentials = service_account.Credentials.from_service_account_info(key_dict)

credentials = service_account.Credentials.from_service_account_file(
    "gen-lang-client-0103422251-0e5b41436c77.json"
)
# print(credentials)
# print("Credentials", credentials)
# vertexai.init(project=project_id, location=location,credentials=credentials)


client = AnthropicVertex(region=location, project_id="886891114006")




def create_chat_function():
    messages = []
    
    def chat(user_input):
        nonlocal messages
        
        messages.append({"role": "user", "content": user_input})
        
        response = client.messages.create(
            model="claude-3-5-sonnet@20240620",
            max_tokens=1024,
            messages=messages,
            system=Prompt,
            temperature = 0.4
        )
        
        assistant_message = response.content[0].text
        
        messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    return chat
