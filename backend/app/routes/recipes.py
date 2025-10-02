from fastapi import APIRouter, Query
from app.services import spoonacular_service

router = APIRouter()

@router.get("/recipes")
def get_recipes(query: str = Query(..., description="Dish or ingredient to search recipes")):
    return spoonacular_service.get_recipes(query)

if __name__ == "__main__":
    print("--- Running Spoonacular Recipe Service Test ---")
    
    # Test 1: Search for a culturally relevant dish
    search_term = "lentil soup"
    search_limit = 3
    print(f"\n[TEST 1] Testing /recipes with query: '{search_term}', limit: {search_limit}...")
    
    try:
        # Call the underlying service function directly
        result = spoonacular_service.get_recipes(search_term, number=search_limit)
        
        if "error" in result:
            print(f"FAIL: Spoonacular Service Failed. Error: {result.get('error')}")
            # This often indicates an invalid API key or exceeded quota (401/402 status codes)
            print(f"  Details: Status Code {result.get('status_code', 'N/A')}")
        else:
            recipes = result.get('results', [])
            print("SUCCESS: Spoonacular Service.")
            print(f"  Total Recipes Found by API: {result.get('totalResults', 'N/A')}")
            
            if recipes:
                first_recipe = recipes[0]
                print(f"  First Recipe Title: {first_recipe.get('title')}")
                print(f"  Recipe ID: {first_recipe.get('id')}")
            else:
                print("  INFO: The query returned no specific recipes in the results list.")
            
    except Exception as e:
        print(f"FAIL: Spoonacular Service Failed due to unhandled Exception: {e}")
