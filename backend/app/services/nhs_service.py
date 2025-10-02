import requests
import json
from typing import Dict, Any, List

# OpenFDA API Base URL (No key needed for basic access)
OPENFDA_BASE_URL = "https://api.fda.gov/drug/label.json"

def search_openfda_pregnancy_labels_simplified(query_term: str):
    """
    Searches OpenFDA drug labels using the most basic and reliable fields.
    """
    
    # SIMPLIFIED QUERY: Search for the term in the indications and usage section.
    search_query = f'indications_and_usage:"{query_term}" OR pregnancy:"{query_term}"'
    
    params = {
        "search": search_query,
        "limit": 5,
        # No 'api_key' parameter needed for public data
    }

    print(f"Searching simplified OpenFDA drug labels for: '{query_term}'...")
    
    try:
        response = requests.get(OPENFDA_BASE_URL, params=params, timeout=20)
        response.raise_for_status() # This will raise HTTPError on 4xx/5xx responses
        
    except requests.exceptions.RequestException as e:
        # Catch any network or timeout errors
        return {"error": "OpenFDA Request failed (Network/Timeout)", "details": str(e)}

    data = response.json()
    results = data.get('results', [])
    
    if not results:
        return {"error": f"No relevant documents found for '{query_term}' in OpenFDA."}

    # Extract key details from the labels
    extracted_data = []
    for result in results:
        product_name = result.get('openfda', {}).get('brand_name', ['N/A'])[0]
        
        # Prioritize the 'pregnancy' section, then fall back to 'warnings' or 'indications'
        pregnancy_text = result.get('pregnancy', [''])[0]
        content_snippet = pregnancy_text or result.get('warnings_and_cautions', [''])[0]
        
        extracted_data.append({
            "Product_Name": product_name,
            "Section_Title": "Pregnancy/Warnings Data",
            "Content_Snippet": content_snippet
        })
            
    return {"success": True, "results": extracted_data}


if __name__ == "__main__":
    search_term = "pregnancy"
    
    result = search_openfda_pregnancy_labels_simplified(search_term)

    if "error" in result:
        print("\n❌ API Error Encountered:")
        print(f"Error: {result['error']}")
        print(f"Details: {result.get('details')}")
    else:
        print("\n✅ SUCCESS: Retrieved OpenFDA Structured Label Data")
        print(f"Found {len(result['results'])} structured documents related to '{search_term}'.")
        print("-" * 30)
        
        if result['results']:
            first_doc = result['results'][0]
            print(f"Document Source (Product): {first_doc['Product_Name']}")
            print(f"Content Type: {first_doc['Section_Title']}")
            # Clean up and print a snippet of the clinical content
            snippet = first_doc['Content_Snippet'].replace('\n', ' ').replace('\r', ' ')
            print(f"Clinical Tip Snippet: {snippet[:400].strip()}...")
        else:
            print("No detailed clinical documents were returned.")