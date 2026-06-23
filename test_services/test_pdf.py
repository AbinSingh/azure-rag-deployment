from app.services.pdf_service import PDFReader

reader = PDFReader()

text = reader.extract_text(
    "downloads/sample.pdf"
)

print(text)