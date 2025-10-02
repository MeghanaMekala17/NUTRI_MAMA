# from transformers import AutoModelForSequenceClassification, AutoTokenizer
# import torch
# import time
# import json

# class SymptomModel:
#     def __init__(self, model_name="microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"):
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

#     def predict(self, text: str):
#         inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#         with torch.no_grad():
#             outputs = self.model(**inputs)
#             probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#         pred_label = torch.argmax(probs, dim=-1).item()
#         confidence = probs[0][pred_label].item()
#         return {"label": str(pred_label), "confidence": confidence}


# if __name__ == "__main__":
#     # --- Code to execute the class and show the response ---
    
#     # Example symptom relevant to maternal health
#     test_text = "Patient reports severe headache and blurred vision. Blood pressure is elevated."
    
#     print("-" * 50)
#     print("STARTING SYMPTOM MODEL TEST")
#     print(f"Test Text: '{test_text}'")
    
#     try:
#         start_time = time.time()
        
#         # 1. Instantiate the Model (This is the long, initial setup step)
#         model_instance = SymptomModel()
        
#         # 2. Call the Predict Method
#         prediction_result = model_instance.predict(test_text)
        
#         end_time = time.time()
        
#         print("-" * 50)
#         print("PREDICTION RESULT:")
#         print(json.dumps(prediction_result, indent=4))
#         print(f"Total execution time: {end_time - start_time:.2f} seconds")
#         print("-" * 50)
        
#     except Exception as e:
#         print("\n\n!!! CRITICAL ERROR DURING MODEL EXECUTION !!!")
#         print("This typically happens during the model loading phase.")
#         print(f"Error Details: {e}")
#         print("\nACTION REQUIRED: Ensure you have authenticated with Hugging Face (`huggingface-cli login`).")

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import time
import json
import os 
from pathlib import Path # Use modern pathlib for robust path construction

# 🛠️ FIX: Define the model path using Pathlib relative to the current script's location.

# 1. Get the path to the directory containing this script (app/models/)
current_file_dir = Path(__file__).parent.resolve()

# 2. Navigate UP to the 'backend' root and then DOWN to the model folder.
# From app/models/ -> UP to app/ -> UP to backend/ -> DOWN to trained_symptom_model/
MODEL_PATH = current_file_dir.parent.parent / "trained_symptom_model" / "final_trained_model"

# Convert to string path for transformers
MODEL_PATH_STR = str(MODEL_PATH)
# ---------------------------------------------------------------------------------

class SymptomModel:
    # 🛠️ Use the explicitly defined local path string
    def __init__(self, model_name=MODEL_PATH_STR):
        print(f"INFO: Attempting to load local trained model from: {model_name}...")
        
        # --- CRITICAL FIX ---
        # The os.path.isdir check is the most direct way to verify the path
        if not os.path.isdir(model_name):
            # If the folder is missing, raise the explicit error with the exact path checked
            raise FileNotFoundError(
                f"Trained model directory not found!\n"
                f"Checked path: {model_name}\n"
                f"ACTION: Ensure your training script ran and the folder exists."
            )

        # Load the model from the verified local disk path
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        print("INFO: Model loading complete.")

    def predict(self, text: str):
        """Processes text and returns prediction label and confidence."""
        # Tokenization
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Post-processing to get probabilities and final prediction
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_label = torch.argmax(probs, dim=-1).item()
        confidence = probs[0][pred_label].item()
        
        return {"label": str(pred_label), "confidence": confidence}


if __name__ == "__main__":
    # --- Code to execute the class and show the response ---
    
    test_text = "Patient reports severe headache and blurred vision. Blood pressure is elevated."
    
    print("-" * 50)
    print("STARTING TRAINED SYMPTOM MODEL TEST")
    
    try:
        start_time = time.time()
        
        # 1. Instantiate the Model 
        model_instance = SymptomModel()
        
        # 2. Call the Predict Method
        prediction_result = model_instance.predict(test_text)
        
        end_time = time.time()
        
        print("-" * 50)
        print("PREDICTION RESULT (Trained Model):")
        print(json.dumps(prediction_result, indent=4)) 
        print(f"Total execution time: {end_time - start_time:.2f} seconds")
        print("-" * 50)
        
    except FileNotFoundError as e:
        print(f"\n\n!!! CRITICAL ERROR: TRAINED MODEL NOT FOUND !!!\n{e}")
        
    except Exception as e:
        print(f"\n\n!!! UNEXPECTED CRITICAL ERROR DURING MODEL EXECUTION !!!\nError Details: {e}")