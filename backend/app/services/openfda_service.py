import requests
import json

BASE_URL = "https://api.fda.gov/drug/label.json"

def check_drug_safety(drug: str):
    params = {"search": f"openfda.generic_name:{drug}", "limit": 1}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "OpenFDA request failed"}

    return response.json()
# --- THE MAIN PART ---
if __name__ == "__main__":
    search_drug = "acetaminophen" # Example: Search for a common drug
    print(f"Searching OpenFDA for drug: '{search_drug}'...")
    
    # Call the function
    result = check_drug_safety(search_drug)
    
    # Process and print the result
    if "error" in result:
        print("\n❌ ERROR:")
        print(json.dumps(result, indent=4))
    else:
        print("\n✅ SUCCESS: Retrieved Drug Label Data")
        # Extract a key detail, like the brand name or warnings
        first_result = result.get('results', [{}])[0]
        brand_name = first_result.get('openfda', {}).get('brand_name', ['N/A'])[0]
        
        # Get the highest-level warning, if available
        warnings = first_result.get('warnings', ['No general warnings section found.'])[0]
        
        print(f"Brand Name Found: {brand_name}")
        print("-" * 30)
        print(f"First Warning Snippet: {warnings[:200].strip()}...")
        
        # Uncomment the line below to see the full JSON response
        print(json.dumps(result, indent=4))
