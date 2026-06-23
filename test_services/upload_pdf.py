from app.services.blob_service import BlobStorage

blob = BlobStorage()

blob.upload_file(
    local_file_path="sample.pdf",
    blob_name="sample.pdf"
)