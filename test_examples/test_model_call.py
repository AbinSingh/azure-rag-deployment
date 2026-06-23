from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

###############################
# Bearer Token Authentication #
###############################

endpoint = "https://abinsinghrajan-7122-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4o-mini"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message)