from app.services.embedding_service import EmbeddingService

embedding = EmbeddingService()

vector = embedding.generate_embedding(
    "Azure Kubernetes Service"
)

print(len(vector))