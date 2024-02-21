import PIL.Image
import google.generativeai as genai
from fastapi import APIRouter
from app.settings import settings
import requests
from io import BytesIO

router = APIRouter(
    prefix="/food_detection",
)


@router.get("/")
def food_detection(img_path: str):
    # set api key retrieved from .env file GEMINI_API_KEY variable
    genai.configure(api_key=settings.GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-pro-vision")

    # TODO : img 어디서 가져올건지? firebase 같은 곳에 올리고 가져오기 ?
    url = img_path.split("images")
    url[1] = url[1].replace("/", "%2F")
    res = requests.get(url[0] + "images" + url[1])
    img = PIL.Image.open(BytesIO(res.content))

    # get food list (e.g. ['apple', 'banana', 'orange'])
    foods = model.generate_content(
        [
            "Extract the food information in the provided image and output them in a list in alphabetical order (if there is no food in provided image, print 'None').",
            img,
        ],
        stream=True,
    )
    foods.resolve()
    foods = (
        (foods.text)
        .replace("*", "")
        .replace("-", " ")
        .replace("\n", "(split)")
        .replace(".", "")
        .split("(split)")
    )
    foods = [food.strip() for food in foods]

    # get leftover decision ('Yes' or 'No')
    leftover_decision = model.generate_content(
        [
            "Are there any leftovers in this photo? (Even if food is left uneaten, if there is food, it is treated as leftover food) Let me know with Yes or No whether this person leave any the food or not.",
            img,
        ],
        stream=True,
    )
    leftover_decision.resolve()
    leftover_decision = (leftover_decision.text).replace(".", "")
    leftover_decision = leftover_decision.strip()

    return foods, leftover_decision


# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("--img_path", type=str)
#     parser.add_argument("--api_key", type=str)

#     args = parser.parse_args()

#     foods, leftover_decision = food_detection(args.img_path, args.api_key)

#     print(f"foods: {foods} \nleftover_decision: {leftover_decision}")
