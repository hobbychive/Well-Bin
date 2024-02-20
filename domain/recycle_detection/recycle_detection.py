import PIL.Image
import google.generativeai as genai
from fastapi import APIRouter
from app.settings import settings

router = APIRouter(
    prefix="/recycle",
)


@router.get("/")
def gemini_recycle_decision(img_path: str):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro-vision")

    img = PIL.Image.open(img_path)

    recycle_decision = model.generate_content(
        [
            "Please let me know if there is anything in this photo that needs separate recycling, along with the location.\n(Answer in this following form : '#. object_name (location in the given image) : bin category'), no additional text",
            img,
        ],
        stream=True,
    )
    recycle_decision.resolve()

    return recycle_decision.text.split("\n")
