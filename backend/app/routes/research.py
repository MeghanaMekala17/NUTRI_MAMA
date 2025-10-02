from fastapi import APIRouter, Query
from app.services import clinicaltrials_service

router = APIRouter()

@router.get("/clinical-trials")
def clinical_trials(condition: str = Query(..., description="Medical condition e.g., 'diabetes'")):
    return clinicaltrials_service.get_trials(condition)

if __name__ == "__main__":
    print("--- Running ClinicalTrials Service Test ---")
    
    # Test 1: Search for a condition relevant to maternal health (e.g., Anemia)
    search_condition = "pregnancy"
    print(f"\n[TEST 1] Testing /clinical-trials with condition: '{search_condition}'...")
    
    try:
        # Call the underlying service function directly
        result = clinicaltrials_service.get_trials(search_condition)
        
        if "error" in result:
            print(f"FAIL: ClinicalTrials Service Failed. Error: {result.get('error')}")
            # The service may return HTTP status details if it failed
            print(f"  Details: {result.get('details', 'N/A')}")
        else:
            # The ClinicalTrials API often returns a 'Study' count
            # total_studies = result.get('FullStudiesResponse', {}).get('NStudiesFound', 'N/A')
            # studies = result.get('FullStudiesResponse', {}).get('FullStudies', [])
            total_found = result.get('totalCount', 'N/A') # Get totalCount directly from the top level
            studies = result.get('studies', [])  
            print("SUCCESS: ClinicalTrials Service.")
            print(f"  Total Studies Found: {total_found}")
            
            if studies:
                # Extract and print key details of the first study
                first_study = studies[0]['Study']
                brief_title = first_study.get('ProtocolSection', {}).get('IdentificationModule', {}).get('BriefTitle', 'No Title')
                status = first_study.get('ProtocolSection', {}).get('StatusModule', {}).get('OverallStatus', 'N/A')
                
                print("--- First Study Details ---")
                print(f"  Title: {brief_title}")
                print(f"  Status: {status}")
            else:
                print("  INFO: The query returned 0 studies.")
            
    except Exception as e:
        print(f"FAIL: ClinicalTrials Service Failed due to unhandled Exception: {e}")
