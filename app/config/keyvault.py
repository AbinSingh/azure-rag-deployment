import os

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

def get_credential():

    environment = os.getenv(
        "ENVIRONMENT",
        "local"
    ).lower()

    if environment == "local":
        return AzureCliCredential()

    return DefaultAzureCredential()

class KeyVaultService:

    def __init__(self):

        vault_url = os.getenv(
            "KEY_VAULT_URL"
        )

        credential = get_credential()

        self.client = SecretClient(
            vault_url=vault_url,
            credential=credential
        )

    def get_secret(
            self,
            secret_name):

        return self.client.get_secret(
            secret_name
        ).value


key_vault = KeyVaultService()