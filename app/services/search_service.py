import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential

from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)
from azure.search.documents.models import VectorizedQuery

from app.config.settings import settings


load_dotenv()


class SearchService:

    def __init__(self):

        self.endpoint = settings.AZURE_SEARCH_ENDPOINT

        self.key = settings.AZURE_SEARCH_API_KEY

        self.index_name = settings.AZURE_SEARCH_INDEX

        credential = AzureKeyCredential(
            self.key
        )

        self.index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=credential
        )

        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=credential
        )

    def create_index(self):

        fields = [

            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True
            ),

            SearchableField(
                name="content",
                type=SearchFieldDataType.String
            ),

            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(
                    SearchFieldDataType.Single
                ),
                searchable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="profile"
            )

        ]

        vector_search = VectorSearch(

            algorithms=[
                HnswAlgorithmConfiguration(
                    name="hnsw"
                )
            ],

            profiles=[
                VectorSearchProfile(
                    name="profile",
                    algorithm_configuration_name="hnsw"
                )
            ]
        )

        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            vector_search=vector_search
        )

        self.index_client.create_or_update_index(
            index
        )

        print("Index Created")

    def upload_documents(
            self,
            docs):

        result = self.search_client.upload_documents(
            documents=docs
        )

        print(result)

    def vector_search(
            self,
            vector):

        vector_query = VectorizedQuery(
            vector=vector,
            k_nearest_neighbors=3,
            fields="embedding"
        )

        results = self.search_client.search(
            search_text=None,
            vector_queries=[
                vector_query
            ]
        )

        output = []

        for item in results:

            output.append(
                item["content"]
            )

        return output