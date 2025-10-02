# import pytest
# from httpx import AsyncClient
# from app.main import app

# @pytest.mark.asyncio
# async def test_nutrition_endpoint():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/api/nutrition/search", params={"query": "apple"})
#     assert response.status_code == 200
#     assert "data" in response.json()

import pytest
# from httpx import AsyncClient
from httpx import ASGITransport,AsyncClient
from app.main import app
import time # Import time if needed, but not strictly for the test logic

@pytest.mark.asyncio
async def test_nutrition_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        # FIX: The correct full path is the prefix (/api/nutrition) + the endpoint path (/nutritionix)
        response = await ac.get("/api/nutrition/nutritionix", params={"query": "apple"})
        
    # 1. Assert Status Code 
    # If the API key is invalid/quota is exceeded, this will be 401/402/500. 
    # We assert 200 for a successful connection and processing.
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"
    
    # 2. Assert Content Structure (Checking for Nutritionix/Spoonacular/OpenFoodFacts keys)
    response_data = response.json()
    
    # Check for a successful data payload key (e.g., 'foods' for Nutritionix, 'results' for Spoonacular)
    assert "foods" in response_data or "results" in response_data or "products" in response_data
    
    # Ensure a list was returned and contains data (check the most likely key first)
    if "foods" in response_data:
        assert len(response_data["foods"]) > 0
    elif "results" in response_data:
        assert len(response_data["results"]) > 0
    elif "products" in response_data:
        assert len(response_data["products"]) > 0