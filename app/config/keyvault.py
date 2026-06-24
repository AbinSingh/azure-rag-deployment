import os

from dotenv import load_dotenv

from azure.identity import ClientSecretCredential

from azure.keyvault.secrets import SecretClient

load_dotenv()


class KeyVaultService:

    def __init__(self):

        vault_url = os.getenv(
            "KEY_VAULT_URL"
        )

        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )

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