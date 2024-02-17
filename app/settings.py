from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    firebase_service_account_path: str = "serviceAccountKey.json"
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY")
    FATSECRET_CLIENT_ID: str = os.environ.get("FATSECRET_CLIENT_ID")
    FATSECRET_CLIENT_SECRET: str = os.environ.get("FATSECRET_CLIENT_SECRET")


settings = Settings()
