from firebase_admin import storage, credentials, initialize_app
from fastapi import APIRouter, UploadFile, File
from app.settings import settings

router = APIRouter(
    prefix="/image",
)

cred = credentials.Certificate(settings.firebase_service_account_path)
default_app = initialize_app(cred, {"storageBucket": "wellbin.appspot.com"})
bucket = storage.bucket()


@router.post("/image_upload")
async def post_image(image: UploadFile = File(...)):
    image_data = await image.read()

    blob = bucket.blob(image.filename)
    blob.upload_from_string(image_data, content_type="image/jpg")
    image_url = blob.public_url

    return {"image_url": image_url}
