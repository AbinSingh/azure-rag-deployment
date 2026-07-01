import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("azure.identity")
logger.setLevel(logging.DEBUG)

from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# token = credential.get_token("https://ai.azure.com/.default")

token = credential.get_token("https://vault.azure.net/.default")