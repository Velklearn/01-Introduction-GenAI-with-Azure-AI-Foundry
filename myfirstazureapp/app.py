# Import main libraries
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# loading variables from .env file
load_dotenv()

# Authenticate the client using your key and endpoint
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-12-01-preview"
)

# Interact with your gpt-5-mini deployment
conversation=[{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("Q:")
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-5-mini", # your deployment name
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")

print(response.choices[0].message.content)