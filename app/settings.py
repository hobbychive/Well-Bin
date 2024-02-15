from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    firebase_service_account_path: str = "serviceAccountKey.json"
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY")


settings = Settings()
