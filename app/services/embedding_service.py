import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class EmbeddingService:

    def __init__(self):

        self.client = OpenAI(
            base_url=os.getenv(
                "AZURE_FOUNDRY_ENDPOINT"
            ),
            api_key=os.getenv(
                "AZURE_FOUNDRY_API_KEY"
            )
        )

        self.model = os.getenv(
            "AZURE_FOUNDRY_EMBEDDING_DEPLOYMENT"
        )

    def generate_embedding(
            self,
            text):

        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        return response.data[0].embedding