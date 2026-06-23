from app.services.pdf_service import PDFReader
from app.services.chunk_service import TextChunker

reader = PDFReader()

chunker = TextChunker()

text = reader.extract_text(
    "downloads/sample.pdf"
)

chunks = chunker.split_text(
    text
)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")

print(chunks[0])