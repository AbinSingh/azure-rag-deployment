import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

##########################
# API Key Authentication #
##########################

client = OpenAI(
    base_url=os.getenv("AZURE_FOUNDRY_ENDPOINT"),
    api_key=os.getenv("AZURE_FOUNDRY_API_KEY")
)

print("Endpoint:", os.getenv("AZURE_FOUNDRY_ENDPOINT"))
print("Deployment:", os.getenv("AZURE_FOUNDRY_EMBEDDING_DEPLOYMENT"))

response = client.embeddings.create(
    model=os.getenv("AZURE_FOUNDRY_EMBEDDING_DEPLOYMENT"),
    input="Azure AI is a cloud AI platform."
)

print("Embedding length:", len(response.data[0].embedding))