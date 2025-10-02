from fastapi import APIRouter, Query
# from app.services import nhs_service
from app.services import nhs_service as drug_label_service 

router = APIRouter()

@router.get("/pregnancy-tips")
def get_pregnancy_tips(week: int = Query(..., description="Pregnancy week (1-40)")):
    return drug_label_service.search_openfda_pregnancy_labels_simplified(str(week))

if __name__ == "__main__":
    print("--- Running Drug Label Service Test ---")
    
    # Test 1: A common week (passed as the search term)
    test_week = 20
    # Note: We are using the imported service name 'drug_label_service' for the test
    print(f"\n[TEST 1] Testing /pregnancy-tips with week (query_term): {test_week}...")
    
    try:
        # Call the underlying service function directly with the correct, existing name
        result = drug_label_service.search_openfda_pregnancy_labels_simplified(str(test_week))
        
        if "error" in result:
            print(f"FAIL: OpenFDA Service Failed. Error: {result.get('error')}")
            print(f"  Details: {result.get('details', 'N/A')}")
        else:
            print("SUCCESS: OpenFDA Drug Label Service.")
            
            # Confirm content presence from the working API structure
            if result.get('results'):
                first_doc = result['results'][0]
                print(f"  Product Name: {first_doc.get('Product_Name', 'N/A')}")
                # Print a snippet of the clinical content
                snippet = first_doc['Content_Snippet'].replace('\n', ' ').replace('\r', ' ')
                print(f"  Snippet: {snippet[:150].strip()}...")
            else:
                print("INFO: Result returned an unknown structure or no documents.")
            
    except Exception as e:
        print(f"FAIL: OpenFDA Service Failed due to unhandled Exception: {e}")