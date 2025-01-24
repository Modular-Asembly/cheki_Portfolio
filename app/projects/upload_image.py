from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from google.cloud import storage
from app.modassembly.storage.get_gcs_bucket import get_gcp_bucket

router = APIRouter()

class ImageUploadResponse(BaseModel):
    url: str

@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)) -> ImageUploadResponse:
    """
    Upload an image to Google Cloud Storage and return the image URL.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        ImageUploadResponse: The URL of the uploaded image.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    bucket = get_gcp_bucket()
    blob = bucket.blob(file.filename)

    # Upload the file to GCS
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Construct the public URL
    url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

    return ImageUploadResponse(url=url)
