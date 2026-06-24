from app.config.keyvault import key_vault
import os

class Settings:
    AZURE_FOUNDRY_ENDPOINT = os.getenv(
        "AZURE_FOUNDRY_ENDPOINT"
    )

    AZURE_CHAT_DEPLOYMENT = os.getenv(
        "AZURE_FOUNDRY_CHAT_DEPLOYMENT"
    )

    AZURE_EMBEDDING_DEPLOYMENT = os.getenv(
        "AZURE_FOUNDRY_EMBEDDING_DEPLOYMENT"
    )

    AZURE_SEARCH_ENDPOINT = os.getenv(
        "AZURE_SEARCH_ENDPOINT"
    )

    AZURE_SEARCH_INDEX = os.getenv(
        "AZURE_SEARCH_INDEX"
    )

    AZURE_STORAGE_CONTAINER = os.getenv(
        "AZURE_STORAGE_CONTAINER"
    )

    CHUNK_SIZE = os.getenv("CHUNK_SIZE")
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP")

    AZURE_FOUNDRY_API_KEY = key_vault.get_secret(
        "azure-foundry-api-key"
    )

    AZURE_SEARCH_API_KEY = key_vault.get_secret(
        "azure-search-api-key"
    )

    AZURE_STORAGE_CONNECTION_STRING = key_vault.get_secret(
        "azure-storage-connection-string"
    )


settings = Settings()