from fastapi import APIRouter, Query
from app.services import nutritionix_service, edamam_service, openfoodfacts_service
import json
import time
router = APIRouter()

@router.get("/nutritionix")
def get_nutritionix(query: str = Query(..., description="Food query e.g., '2 eggs and toast'")):
    return nutritionix_service.get_nutrition_data(query)

@router.get("/edamam")
def get_edamam(ingredient: str = Query(..., description="Ingredient name")):
    return edamam_service.get_nutrition_info(ingredient)

@router.get("/openfoodfacts")
def get_openfoodfacts(item: str = Query(..., description="Food item name")):
    return openfoodfacts_service.search_food(item)

if __name__ == "__main__":
    print("--- Running External Nutrition Service Tests ---")
    
    # --- TEST 1: Nutritionix Service (Natural Language Query) ---
    print("\n[TEST 1] Testing /nutritionix with query: '1 apple and 1 cup of milk'...")
    try:
        nutritionix_result = nutritionix_service.get_nutrition_data("1 apple and 1 cup of milk")
        
        if "error" in nutritionix_result:
            print(f"FAIL: Nutritionix Failed: {nutritionix_result.get('error')}")
        elif nutritionix_result.get('foods'):
            first_food = nutritionix_result['foods'][0]
            print("SUCCESS: Nutritionix.")
            print(f"   First Item: {first_food.get('food_name')}")
            print(f"   Calories: {first_food.get('nf_calories')} kcal")
        else:
            print("INFO: Nutritionix returned no foods.")
            
    except Exception as e:
        print(f"FAIL: Nutritionix Service Failed due to Exception: {e}")

    # --- Pause to respect potential rate limits ---
    time.sleep(1) 
    
    # --- TEST 2: Edamam Service (Ingredient Search) ---
    print("\n[TEST 2] Testing /edamam with ingredient: 'cottage cheese'...")
    try:
        edamam_result = edamam_service.get_nutrition_info("cottage cheese")
        
        if "error" in edamam_result:
            print(f"FAIL: Edamam Failed: {edamam_result.get('error')}")
        elif edamam_result.get('hints'):
            first_match = edamam_result['hints'][0]['food']
            print("SUCCESS: Edamam.")
            print(f"   Food ID: {first_match.get('foodId')}")
            print(f"   Category: {first_match.get('category')}")
        else:
            print("INFO: Edamam returned no hints.")
            
    except Exception as e:
        print(f"FAIL: Edamam Service Failed due to Exception: {e}")

    # --- Pause to respect potential rate limits ---
    time.sleep(1) 

    # --- TEST 3: OpenFoodFacts Service (Product Search) ---
    print("\n[TEST 3] Testing /openfoodfacts with item: 'dal makhani'...")
    try:
        off_result = openfoodfacts_service.search_food("dal makhani")
        
        if "error" in off_result:
            print(f"FAIL: OpenFoodFacts Failed: {off_result.get('error')}")
        elif off_result.get('products'):
            first_product = off_result['products'][0]
            print("SUCCESS: OpenFoodFacts.")
            print(f"   Product Name: {first_product.get('product_name', 'N/A')}")
            print(f"   NutriScore: {first_product.get('nutrition_grade_fr', 'N/A').upper()}")
        else:
            print("INFO: OpenFoodFacts returned no products.")
            
    except Exception as e:
        print(f"FAIL: OpenFoodFacts Service Failed due to Exception: {e}")
