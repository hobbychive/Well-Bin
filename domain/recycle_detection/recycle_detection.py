import PIL.Image
import google.generativeai as genai
from fastapi import APIRouter
from app.settings import settings
import requests
from io import BytesIO

router = APIRouter(
    prefix="/recycle",
)


@router.get("/")
def gemini_recycle_decision(img_path: str):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro-vision")

    url = img_path.split("images")
    url[1] = url[1].replace("/", "%2F")
    res = requests.get(url[0] + "images" + url[1])
    img = PIL.Image.open(BytesIO(res.content))

    recycle_decision = model.generate_content(
        [
            "Please let me know if there is anything in this photo that needs separate recycling, along with the location.\n(Answer in this following form : '#. object_name (location in the given image) : bin category'), with no additional text other than the form.",
            img,
        ],
        stream=True,
    )
    recycle_decision.resolve()

    return recycle_decision.text.split("\n")
