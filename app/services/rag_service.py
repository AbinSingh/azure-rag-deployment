from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.chat_service import ChatService


class RAGService:

    def __init__(self):

        self.embedding = EmbeddingService()

        self.search = SearchService()

        self.chat = ChatService()

    def ask(
            self,
            question):

        question_vector = self.embedding.generate_embedding(
            question
        )

        chunks = self.search.vector_search(
            question_vector
        )

        context = "\n\n".join(
            chunks
        )

        prompt = f"""

                Use the following context to answer.
                
                Context:
                -------------------
                
                {context}
                
                -------------------
                
                Question:
                
                {question}
                
                Answer:
                """

        answer = self.chat.ask(
            prompt
        )

        return answer