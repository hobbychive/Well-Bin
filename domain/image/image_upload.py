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
    # 이미지를 읽어옴
    image_data = await image.read()

    # 이미지를 Firebase Storage에 업로드
    blob = bucket.blob(image.filename)
    blob.upload_from_string(
        image_data, content_type="image/jpg"
    )  # 이미지 타입에 맞게 content_type을 설정

    # 이미지 URL을 반환
    image_url = blob.public_url

    return {"image_url": image_url}
