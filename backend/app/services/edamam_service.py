import requests

# 🔑 Put your API credentials directly here
EDAMAM_APP_ID = ""
EDAMAM_APP_KEY = ""

BASE_URL = "https://api.edamam.com/api/nutrition-data"

def get_nutrition_info(ingredient: str):
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "ingr": ingredient
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "Edamam request failed", "status_code": response.status_code}

    return response.json()


if __name__ == "__main__":
    # ✅ Test with an example
    print(get_nutrition_info("1 cup rice"))
