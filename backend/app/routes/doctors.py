# from fastapi import APIRouter, Query
# from ..services import ipinfo_service, nominatim_service

# router = APIRouter()

# @router.get("/my-location")
# def get_my_location():
#     return ipinfo_service.get_ip_details()

# @router.get("/search-location")
# def search_location(query: str = Query(..., description="Location name e.g., 'London hospital'")):
#     return nominatim_service.get_location(query)
from fastapi import APIRouter, Query
from app.services import ipinfo_service, nominatim_service
import json # Import json for cleaner test output

router = APIRouter()

@router.get("/my-location")
def get_my_location():
    return ipinfo_service.get_ip_details()

@router.get("/search-location")
def search_location(query: str = Query(..., description="Location name e.g., 'London hospital'")):
    return nominatim_service.get_location(query)


if __name__ == "__main__":
    print("--- Running Service Tests ---")
    
    # 1. Test the /my-location functionality
    print("\n[TEST 1] Testing /my-location (IP Details)...")
    try:
        ip_details_result = ipinfo_service.get_ip_details()
        print(f"IP Service Success. Status: {ip_details_result.get('status', 'N/A')}")
        # Print a key piece of information
        print(f"   IP Address: {ip_details_result.get('ip', 'N/A')}")
        print(f"   City: {ip_details_result.get('city', 'N/A')}")
        
    except Exception as e:
        print(f"IP Service Failed: {e}")
    
    # 2. Test the /search-location functionality
    search_term = "Hyderabad, India"
    print(f"\n[TEST 2] Testing /search-location (Nominatim) for: '{search_term}'...")
    try:
        location_result = nominatim_service.get_location(search_term)
        
        if "error" in location_result:
            print(f"Nominatim Service Failed: {location_result['error']}")
        elif location_result and isinstance(location_result, list):
            first_match = location_result[0]
            print("Nominatim Service Success.")
            print(f"   Display Name: {first_match.get('display_name', 'N/A')}")
            print(f"   Coordinates: ({first_match.get('lat', 'N/A')}, {first_match.get('lon', 'N/A')})")
        else:
            print("Nominatim Service returned no results or an unexpected format.")
            
    except Exception as e:
        print(f" Nominatim Service Failed: {e}")