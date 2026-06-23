from fastapi import FastAPI

from app.services.rag_service import RAGService

app = FastAPI(
    title="Azure RAG API",
    version="1.0.0"
)

rag = RAGService()

# Health endpoint
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.get("/")
def home():

    return {
        "message": "Azure RAG API Running"
    }

@app.post("/chat")
def chat(
        question: str):

    answer = rag.ask(
        question
    )

    return {
        "question": question,
        "answer": answer
    }