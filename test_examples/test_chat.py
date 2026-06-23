import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

##########################
# API Key Authentication #
##########################

client = OpenAI(
    base_url=os.getenv("AZURE_FOUNDRY_ENDPOINT"),
    api_key=os.getenv("AZURE_FOUNDRY_API_KEY"))

response = client.chat.completions.create(
    model=os.getenv("AZURE_FOUNDRY_CHAT_DEPLOYMENT"),
    messages=[
        {
            "role": "user",
            "content": "Explain Azure Kubernetes Service."
        }
    ]
)

print(response.choices[0].message.content)