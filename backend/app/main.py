from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes import (
    nutrition,
    recipes,
    pregnancy,
    symptom,
    doctors,
    geolocation,
    safety,
    research,
    guidance
)

app = FastAPI(
    title="NutriMama API",
    description="Backend API for nutrition, pregnancy, symptom checker, safety, and research.",
    version="1.0.0",
)

# Enable CORS (allow frontend React app to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recipes"])
app.include_router(pregnancy.router, prefix="/api/pregnancy", tags=["Pregnancy"])
app.include_router(symptom.router, prefix="/api/symptom", tags=["Symptom Checker"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(geolocation.router, prefix="/api/geolocation", tags=["Geolocation"])
app.include_router(safety.router, prefix="/api/safety", tags=["Drug Safety"])
app.include_router(research.router, prefix="/api/research", tags=["Clinical Research"])
app.include_router(guidance.router, prefix="/api/guidance", tags=["AI Guidance"])
@app.get("/")
def root():
    return {"message": "NutriMama API is running 🚀"}
