# import pytest
# from httpx import AsyncClient
# from app.main import app

# @pytest.mark.asyncio
# async def test_pregnancy_tips_endpoint():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/api/pregnancy/tips")
#     assert response.status_code == 200
#     assert isinstance(response.json().get("tips"), list)

import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_pregnancy_tips_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Requesting a specific week and using the assumed correct path
        response = await ac.get(
            "/api/pregnancy/pregnancy-tips", 
            params={"week": 20}
        )
    
    # 1. Assert Status Code (Must be 200)
    assert response.status_code == 200
    
    data = response.json()
    
    # --- FIX 1: Assert the actual top-level success key ---
    # The OpenFDA service returns 'success': True/False, not 'status': 'success'
    assert data.get("success") is True 
    
    # --- FIX 2: Assert the actual list key and its type ---
    # The OpenFDA service uses the key 'results' for the list of documents
    assert "results" in data 
    assert isinstance(data["results"], list) 
    
    # Ensure at least one document (drug label) was found
    assert len(data["results"]) > 0