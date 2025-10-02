from fastapi import APIRouter, Query
from app.services import openfda_service

router = APIRouter()

@router.get("/drug-safety")
def drug_safety(drug: str = Query(..., description="Drug name e.g., 'Paracetamol'")):
    return openfda_service.check_drug_safety(drug)

if __name__ == "__main__":
    print("--- Running OpenFDA Drug Safety Service Test ---")
    
    # Test 1: Search for a common, known drug (Acetaminophen is often used clinically)
    search_drug = "acetaminophen" 
    print(f"\n[TEST 1] Testing /drug-safety with drug: '{search_drug}'...")
    
    try:
        # Call the underlying service function directly
        result = openfda_service.check_drug_safety(search_drug)
        
        if "error" in result:
            print(f"FAIL: OpenFDA Service Failed. Error: {result.get('error')}")
            # Print details if a non-200 status code was returned
            print(f"  Details: {result.get('details', 'N/A')}")
        else:
            print("SUCCESS: OpenFDA Service.")
            
            # Extract and print key details from the first result
            first_doc = result.get('results', [{}])[0]
            product_name = first_doc.get('openfda', {}).get('brand_name', ['N/A'])[0]
            warnings_section = first_doc.get('warnings', [''])[0]
            
            print(f"  Brand Name: {product_name}")
            # Clean up and print a snippet of the clinical content
            snippet = warnings_section.replace('\n', ' ').replace('\r', ' ')
            print(f"  Warning Snippet: {snippet[:150].strip()}...")
            
    except Exception as e:
        print(f"FAIL: OpenFDA Service Failed due to unhandled Exception: {e}")