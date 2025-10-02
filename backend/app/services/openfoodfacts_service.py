import requests
import json

BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"

def search_food(item: str):
    params = {
        "search_terms": item,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "OpenFoodFacts request failed"}

    return response.json()

# main part included for testing

if __name__ == "__main__":
    # This part will only execute when the script is run directly.
    search_term = "paneer"
    print(f"Searching OpenFoodFacts for: '{search_term}'...")
    
    # Call the function
    data = search_food(search_term)
    
    # Output the result in a readable format
    if "error" in data:
        print("\n❌ ERROR:")
        print(json.dumps(data, indent=4))
    else:
        product_count = data.get('count', 0)
        products = data.get('products', [])
        print(f"\n✅ SUCCESS: Found {product_count} total products.")
        
        if products:
            # Print details for the first product
            first_product = products[0]
            print(f"--- First Product Details ---")
            print(f"Name: {first_product.get('product_name', 'N/A')}")
            print(f"Barcode: {first_product.get('code', 'N/A')}")
            print(f"NutriScore: {first_product.get('nutrition_grade_fr', 'N/A').upper()}")
        else:
            print("No detailed products were returned.")
