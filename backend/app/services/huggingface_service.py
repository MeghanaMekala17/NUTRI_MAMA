from app.models.symptom_model import SymptomModel
import json
import time

symptom_model = SymptomModel()

def analyze_symptoms(text: str):
    return symptom_model.predict(text)

if __name__ == '__main__':
    # Test case: Symptoms related to potential preeclampsia
    test_symptom = "Patient reports severe headache and high blood pressure."
    
    print("-" * 50)
    print("STARTING ANALYZE SYMPTOMS SERVICE TEST")
    print(f"Test Text: '{test_symptom}'")
    
    start_time = time.time()
    
    try:
        # Call the service function
        test_result = analyze_symptoms(test_symptom)
        
        end_time = time.time()
        
        if "error" in test_result:
            print(f"[FAIL] SERVICE FAIL: {test_result['error']}")
        else:
            print("-" * 50)
            print("[SUCCESS] SERVICE SUCCESS: Prediction Received")
            print(json.dumps(test_result, indent=4))
        
        print(f"\nTotal execution time (including model access): {end_time - start_time:.2f} seconds")
        
    except NameError:
        print("\n[FAIL] CRITICAL FAIL: The symptom_model object or the service function is not defined.")
    except Exception as e:
        # This will catch errors during the prediction or model loading
        print(f"\n[FAIL] UNHANDLED EXCEPTION: Service crashed. Details: {e}")
        
    print("-" * 50)