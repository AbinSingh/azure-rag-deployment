from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService

embedding = EmbeddingService()

search = SearchService()

question = "In which company Abin working at present and what is his major project"

vector = embedding.generate_embedding(
    question
)

results = search.vector_search(
    vector
)

print()

print("Retrieved Chunks")

print()

for index, chunk in enumerate(results):

    print(
        f"Chunk {index+1}"
    )

    print(chunk)

    print("-" * 60)