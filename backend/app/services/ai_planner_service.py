import json
from typing import Dict, Any, List
from google import genai
from google.genai.errors import APIError

# Hardcoded API key as requested
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

class AIPlannerService:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        self.client = None
        
        if not GEMINI_API_KEY:
            return
        
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception:
            self.client = None

    import json
class AIPlannerService:
    def init(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        self.client = None
        
        if not GEMINI_API_KEY:
             return
             
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception:
            self.client=None

    def generate_meal_guidance(self, trimester, anemia_risk, user_region, comorbidities, supplements, literacy_level):
        # Placeholder logic for demonstration
        # You should replace this with your actual meal planning logic.
        guidance = {
            "trimester": trimester,
            "anemia_risk": anemia_risk,
            "user_region": user_region,
            "comorbidities": comorbidities,
            "supplements": supplements,
            "literacy_level": literacy_level,
            "recommended_meals": [
                "Iron-rich spinach dal",
                "Protein-packed lentils",
                "Vitamin C rich citrus fruits"
            ],
            "advice": "Ensure plenty of hydration and regular meals."
        }
        return guidance
        
def collect_user_input():
    try:
        trimester = int(input("Enter current trimester (1, 2, or 3): "))
        anemia_risk = input("Is there anemia risk? (yes/no): ").strip().lower() == "yes"
        user_region = input("Enter your region (e.g., North India, South India): ").strip()
        comorbidities = input("List known comorbidities (comma-separated, or 'none'): ").strip()
        comorbidities_list = [c.strip() for c in comorbidities.split(",")] if comorbidities.lower() != "none" else []
        supplements = input("List current supplements (comma-separated, or 'none'): ").strip()
        supplements_list = [s.strip() for s in supplements.split(",")] if supplements.lower() != "none" else []
        literacy_level = input("Enter literacy level (Low/Medium/High): ").strip().capitalize()
        return {
            "trimester": trimester,
            "anemia_risk": anemia_risk,
            "user_region": user_region,
            "comorbidities": comorbidities_list,
            "supplements": supplements_list,
            "literacy_level": literacy_level
        }
    except Exception as e:
        print(f"Error collecting input: {e}")
        return None

def main():
    user_data = collect_user_input()  # You must define this function
    if user_data:
        planner = AIPlannerService()
        result = planner.generate_meal_guidance(
            trimester=user_data["trimester"],
            anemia_risk=user_data["anemia_risk"],
            user_region=user_data["user_region"],
            comorbidities=user_data["comorbidities"],
            supplements=user_data["supplements"],
            literacy_level=user_data["literacy_level"]
        )
        print("\n--- Personalized Meal Guidance Output ---")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("No input provided or an error occurred.")
        return None

# Fix the if condition for execution
if __name__ == "__main__":
    main()
