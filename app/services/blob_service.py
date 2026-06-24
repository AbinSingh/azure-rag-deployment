from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from app.config.settings import settings

load_dotenv()


class BlobStorage:

    def __init__(self):

        self.connection_string = settings.AZURE_STORAGE_CONNECTION_STRING

        self.container_name = settings.AZURE_STORAGE_CONTAINER


        self.client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

        self.container_client = self.client.get_container_client(
            self.container_name
        )

    def upload_file(self,
                    local_file_path,
                    blob_name):

        with open(local_file_path, "rb") as data:

            self.container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=True
            )

        print(f"Uploaded {blob_name}")

    def download_file(self,
                      blob_name,
                      download_path):

        blob_client = self.container_client.get_blob_client(
            blob_name
        )

        with open(download_path, "wb") as file:

            file.write(
                blob_client.download_blob().readall()
            )

        print(f"Downloaded {blob_name}")