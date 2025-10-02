from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
# Ensure this import path matches your project structure
from app.services.ai_planner_service import AIPlannerService 

router = APIRouter()

# --- 1. Define the Input Data Model (Schema for Frontend) ---
class GuidanceRequest(BaseModel):
    trimester: int = Field(..., ge=1, le=3, description="Current trimester of pregnancy (1-3)")
    anemia_risk: bool = Field(False, description="True if anemia is detected or high risk.")
    user_region: str = Field(..., description="User's geographic region (e.g., 'North India', 'South India')")
    comorbidities: List[str] = Field([], description="List of chronic conditions (e.g., 'Gestational Diabetes')")
    supplements: List[str] = Field([], description="List of supplements being taken (e.g., 'Calcium 500mg')")
    literacy_level: str = Field("Medium", description="User's literacy ('Low' or 'Medium/High')")

# --- 2. Initialize the Service ONCE ---
try:
    planner_service = AIPlannerService()
except Exception as e:
    # Log critical failure but allow app to start
    print(f"CRITICAL: AI Planner failed to initialize at startup: {e}")
    planner_service = None


@router.post("/meal-guidance", tags=["AI Guidance"])
def get_ai_meal_guidance(request: GuidanceRequest):
    """
    Generates a personalized, structured meal plan recommendation using the Gemini AI Planner.
    This endpoint is designed for frontend consumption.
    """
    if planner_service is None:
        return {"status": "error", "message": "AI Planner is not available."}
        
    # Call the service function with the unpacked request data
    return planner_service.generate_meal_guidance(
        trimester=request.trimester,
        anemia_risk=request.anemia_risk,
        user_region=request.user_region,
        comorbidities=request.comorbidities,
        supplements=request.supplements,
        literacy_level=request.literacy_level
    )