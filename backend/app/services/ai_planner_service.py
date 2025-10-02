import os
import json
import time
from typing import Dict, Any, List
from google import genai
from google.genai.errors import APIError

# 🔑 WARNING: API Key is hardcoded as requested.
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

# --- KNOWLEDGE BASE SNIPPETS ---
ICMR_GUIDANCE = """
1. Trimester 1 (Weeks 1-12): Focus on Folate, Vitamin B6.
2. Trimester 2 (Weeks 13-27): Focus on Iron, Calcium.
3. Iron-Rich Indian Foods: Lentils (dal), Spinach (palak), Jaggery (gud), Ragi, Poha, Red Meat/Liver.
4. Calcium-Rich Indian Foods: Curds (Dahi), Paneer, Milk, Tofu, Ragi.
5. Dietary Constraints: Avoid simple sugars and high glycemic index foods for Gestational Diabetes. Calcium inhibits iron absorption; consume iron and calcium meals at least 2 hours apart.
"""
# ---------------------------------

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

    def generate_meal_guidance(self, 
                              trimester: int, 
                              anemia_risk: bool, 
                              user_region: str,
                              comorbidities: List[str],
                              supplements: List[str],
                              literacy_level: str) -> Dict[str, Any]:
        """
        Generates personalized, structured meal guidance.
        """
        if not self.client:
            return {"status": "error", "message": "AI client not available. Key missing or invalid."}

        # --- CONSOLIDATED PROMPT (Forces Structured Output) ---
        user_prompt = f"""
        # INSTRUCTION: You are an expert Indian maternal nutritionist. Provide culturally relevant, 
        trimester-specific meal recommendations based strictly on the ICMR guidelines and user constraints. 
        Your ENTIRE RESPONSE MUST be a SINGLE, VALID JSON OBJECT, with NO TEXT BEFORE OR AFTER.

        # User Profile:
        Current Trimester: {trimester}
        Anemia Risk: {anemia_risk}
        Known Comorbidities: {', '.join(comorbidities) or 'None'}
        Current Supplements: {', '.join(supplements) or 'None'}
        User's Region: {user_region}
        Literacy Level: {literacy_level}
        
        # ICMR/WHO Guidelines (Internal Reference):
        {ICMR_GUIDANCE}
        
        # Output Structure and Content Rules:
        1. Determine the top priority nutrient.
        2. Suggest ONE specific Indian dish/food item appropriate for the region.
        3. Consolidate ALL safety notes (diabetes/calcium timing) and nutritional justification into a single field named 'comprehensive_advice_for_asha'.
        4. If the literacy level is 'Low', keep the language in 'comprehensive_advice_for_asha' very simple.
        5. If 'Anemia Risk' is True, prioritize Iron above all else.
        """
        
        # --- DEFINE JSON SCHEMA ---
        output_schema = {
            "type": "object",
            "properties": {
                "priority_nutrient": {"type": "string"},
                "suggested_food_item": {"type": "string"},
                "comprehensive_advice_for_asha": {"type": "string"}
            },
            "required": ["priority_nutrient", "suggested_food_item", "comprehensive_advice_for_asha"]
        }
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt, 
                config={
                    "response_mime_type": "application/json",
                    "response_schema": output_schema,
                    "temperature": 0.3
                }
            )
            
            text_response = response.text.strip()
            
            # Final parsing attempt
            if text_response.startswith('```json'):
                text_response = text_response.strip('```json').strip('```').strip()
            
            guidance_data = json.loads(text_response)
            
            return {"status": "success", "guidance": guidance_data}
        
        except APIError as e:
            return {"status": "error", "message": f"Gemini API Error (Quota/Key Issue): {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Parsing/Unexpected Error: {e}"}