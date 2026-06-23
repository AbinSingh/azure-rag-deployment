import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatService:

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
            "AZURE_FOUNDRY_CHAT_DEPLOYMENT"
        )

    def ask(
            self,
            prompt):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    You are a helpful AI assistant.
                    Answer only from the supplied context.
                    If the answer is not present,
                    say you do not know.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content