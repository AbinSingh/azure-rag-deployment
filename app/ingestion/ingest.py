import uuid

from app.services.pdf_service import PDFReader
from app.services.chunk_service import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService

reader = PDFReader()

chunker = TextChunker()

embedding = EmbeddingService()

search = SearchService()

text = reader.extract_text(
    "downloads/sample.pdf"
)

chunks = chunker.split_text(
    text
)

# create index
search.create_index()

documents = []

for chunk in chunks:

    vector = embedding.generate_embedding(
        chunk
    )

    documents.append(
        {
            "id": str(uuid.uuid4()),
            "content": chunk,
            "embedding": vector
        }
    )

search.upload_documents(
    documents
)

print("Upload Completed")