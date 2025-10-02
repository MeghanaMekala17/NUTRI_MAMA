# from fastapi import APIRouter, Query
# from app.services import huggingface_service
# import json
# import time

# router = APIRouter()

# @router.get("/symptom-checker")
# def symptom_checker(symptom: str = Query(..., description="Symptom description e.g., 'headache and fever'")):
#     return huggingface_service.run_model("distilbert-base-uncased-finetuned-sst-2-english", symptom)

# if __name__ == "__main__":
#     print("--- Running Hugging Face Symptom Service Test ---")
    
#     # Test 1: A sample symptom string
#     test_symptom = "Patient reports severe fatigue and persistent vomiting."
#     test_model_id = "distilbert-base-uncased-finetuned-sst-2-english"
    
#     # NOTE: This model is for sentiment analysis, not medical classification.
#     # The test confirms the API call structure is correct.
    
#     print(f"\n[TEST 1] Testing /symptom-checker with symptom: '{test_symptom}'...")
#     print(f"   Model ID: {test_model_id}")
    
#     start_time = time.time()
    
#     try:
#         # Call the underlying service function directly
#         result = huggingface_service.run_model(test_model_id, test_symptom)
        
#         end_time = time.time()
        
#         if "error" in result:
#             print(f"FAIL: Hugging Face Service Failed. Error: {result.get('error')}")
#             # Print details if a specific status code was returned
#             print(f"  Details: {result.get('details', 'N/A')}")
#         else:
#             print("SUCCESS: Hugging Face Service.")
            
#             # Print key prediction details based on the expected output structure
#             print("--- Prediction Details ---")
#             print(json.dumps(result, indent=4))
            
#     except Exception as e:
#         print(f"FAIL: Hugging Face Service Failed due to unhandled Exception: {e}")

#     print(f"\nTotal test execution time: {end_time - start_time:.2f} seconds")

# Assuming this is the content of app/routes/symptom.py

from fastapi import APIRouter, Query
from app.services import huggingface_service
import json
import time

router = APIRouter()

@router.get("/symptom-checker")
def symptom_checker(symptom: str = Query(..., description="Symptom description e.g., 'headache and fever'")):
    # FIX A: The router should call the correct function name
    return huggingface_service.analyze_symptoms(symptom) 


if __name__ == "__main__":
    
    # FIX B: Initialize end_time safely outside the try block
    start_time = time.time()
    end_time = start_time 
    
    test_symptom = "Patient reports severe fatigue and persistent vomiting."
    
    # ... (print statements removed for brevity) ...

    try:
        # FIX C: Call the correctly named function in the test block
        result = huggingface_service.analyze_symptoms(test_symptom) 
        
        # FIX D: Update end_time only upon successful service call completion
        end_time = time.time() 
        
        # ... (rest of success/fail print logic) ...
        
    except AttributeError:
        # This will now catch the 'no attribute run_model' if the service file 
        # definition is messed up, but it shouldn't happen if FIX A/C is correct.
        print("FAIL: Check function name and imports.")

    # This line now runs without the NameError
    print(f"\nTotal test execution time: {end_time - start_time:.2f} seconds")