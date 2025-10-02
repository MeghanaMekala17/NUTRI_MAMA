import requests
import json
from typing import Dict, Any, List

# 🔑 WARNING: This key is hardcoded and exposed. Replace this placeholder 
# with your actual Spoonacular API Key if you use this code.
SPOONACULAR_API_KEY = "YOUR_HARDCODE" 

# The endpoint for searching recipes
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

def get_recipes(query: str, number: int = 5):
    """
    Fetch recipes from Spoonacular API using the hardcoded key.
    :param query: The food/dish to search (e.g., "lentil soup")
    :param number: Number of results to return (default=5)
    """
    # Check if the placeholder was accidentally left empty
    if not SPOONACULAR_API_KEY or SPOONACULAR_API_KEY == "c8c6c670f5124c27a0dbb84380b2e58f":
        return {"error": "API Key is missing or default placeholder key is used.", "status_code": 500}

    params = {
        "query": query,
        "number": number,
        "apiKey": SPOONACULAR_API_KEY,
        "cuisine": "Indian"
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": "Network or Request Error", "details": str(e)}

    # Handle API-specific errors (401 for invalid key, 402 for quota exceeded)
    if response.status_code == 401:
        return {"error": "Unauthorized or Invalid API Key", "status_code": 401}
    if response.status_code == 402:
        return {"error": "Daily points quota exceeded", "status_code": 402}
    if response.status_code != 200:
        return {"error": "Spoonacular request failed", "status_code": response.status_code, "response_text": response.text}

    return response.json()


if __name__ == "__main__":
    search_query = "lentil soup"
    search_count = 3
    
    print("--- Running Spoonacular Service Test (Hardcoded Key) ---")
    print(f"[TEST] Testing get_recipes with query: '{search_query}'...")
    
    result = get_recipes(search_query, number=search_count)
    
    if "error" in result:
        print("\nFAIL: Spoonacular Service Failed.")
        print(f"Error: {result.get('error')}")
        print(f"Status Code: {result.get('status_code', 'N/A')}")
    else:
        recipes = result.get('results', [])
        print("\nSUCCESS: Spoonacular Service.")
        print(f"Total Results Found: {result.get('totalResults', 'N/A')}")
        
        if recipes:
            first_recipe = recipes[0]
            print("--- First Recipe Details ---")
            print(f"Title: {first_recipe.get('title')}")
            print(f"ID: {first_recipe.get('id')}")
        else:
            print("INFO: The query returned no specific recipes.")