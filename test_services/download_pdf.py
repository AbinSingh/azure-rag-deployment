from app.services.blob_service import BlobStorage

blob = BlobStorage()

blob.download_file(
    blob_name="sample.pdf",
    download_path="../app/ingestion/downloads/sample.pdf"
)