import requests

# ⚠️ Replace with your actual credentials
NUTRITIONIX_APP_ID ="" 
NUTRITIONIX_APP_KEY = ""

BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

def get_nutrition_data(query: str):
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json"
    }
    body = {"query": query}

    response = requests.post(BASE_URL, headers=headers, json=body)
    
    if response.status_code != 200:
        return {"error": f"Nutritionix request failed: {response.text}"}

    return response.json()
if __name__ == "__main__":
    # Test query
    query = "1 cup rice"
    result = get_nutrition_data(query)
    print(result)
