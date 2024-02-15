from fastapi import FastAPI
from firebase_admin import credentials, initialize_app

from app.settings import settings

from domain.food_detection import food_detection_router
from domain.image import image_upload

app = FastAPI()

# # Firebase 초기화
# cred = credentials.Certificate(settings.firebase_service_account_path)
# default_app = initialize_app(cred, {"storageBucket": "wellbin.appspot.com"})

app.include_router(food_detection_router.router)
app.include_router(image_upload.router)
