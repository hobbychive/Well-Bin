from fatsecret import Fatsecret
from app.settings import settings
from fastapi import APIRouter
from difflib import SequenceMatcher

router = APIRouter(
    prefix="/nutrition",
)

fs = Fatsecret(settings.FATSECRET_CLIENT_ID, settings.FATSECRET_CLIENT_SECRET)


@router.get("/")
def nutrition_search(food: str):
    foods = fs.foods_search(food)
    best_match = 0
    index = 0
    for i in range(len(foods)):
        diff = SequenceMatcher(None, food, foods[i]["food_name"]).ratio()
        if diff > best_match and foods[i]["food_type"] == "Generic":
            best_match = diff
            index = i
    target_id = foods[index]["food_id"]
    food_details = fs.food_get(target_id)
    index = 0
    for i in range(len(food_details["servings"]["serving"])):
        if food_details["servings"]["serving"][i]["serving_description"] == "100 g":
            index = i
            break
    target = food_details["servings"]["serving"][index]

    target.pop("serving_id")
    target.pop("serving_url")
    target.pop("metric_serving_amount")
    target.pop("number_of_units")
    target.pop("measurement_description")
    target.pop("metric_serving_unit")

    return target
