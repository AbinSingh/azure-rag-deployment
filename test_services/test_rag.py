from app.services.rag_service import RAGService

rag = RAGService()

answer = rag.ask(
    "In which company Abin working at present and what is his major project"
)

print()

print(answer)