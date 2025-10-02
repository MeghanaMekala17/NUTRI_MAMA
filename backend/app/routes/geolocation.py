from fastapi import APIRouter, Query
from app.services import ipinfo_service, nominatim_service
import json
import time

router = APIRouter()

@router.get("/ip-details")
def get_ip(ip: str = ""):
    return ipinfo_service.get_ip_details(ip)

@router.get("/geo-search")
def geo_search(query: str = Query(...)):
    return nominatim_service.get_location(query)


if __name__ == "__main__":
    print("--- Running Geolocation Service Tests ---")
    
    # 1. Test the /ip-details functionality
    print("\n[TEST 1] Testing /ip-details (Current IP details)...")
    try:
        # Pass an empty string to get details for the current public IP
        ip_details_result = ipinfo_service.get_ip_details("")
        
        if "error" in ip_details_result:
            print(f"FAIL: IP Service Failed: {ip_details_result.get('error')}")
        else:
            print("SUCCESS: IP Service.")
            print(f"   IP Address: {ip_details_result.get('ip', 'N/A')}")
            print(f"   Location: {ip_details_result.get('city', 'N/A')}, {ip_details_result.get('country', 'N/A')}")
            
    except Exception as e:
        print(f"FAIL: IP Service Failed due to Exception: {e}")
    
    # --- IMPORTANT: Wait 1 second to respect Nominatim rate limit (1 request/second) ---
    time.sleep(1) 
    
    # 2. Test the /geo-search functionality
    search_term = "Hyderabad, India"
    print(f"\n[TEST 2] Testing /geo-search (Nominatim) for: '{search_term}'...")
    try:
        location_result = nominatim_service.get_location(search_term)
        
        if "error" in location_result:
            print(f"FAIL: Nominatim Service Failed: {location_result.get('error')}")
        elif location_result and isinstance(location_result, list):
            first_match = location_result[0]
            print("SUCCESS: Nominatim Service.")
            print(f"   Display Name: {first_match.get('display_name', 'N/A')}")
            print(f"   Coordinates: ({first_match.get('lat', 'N/A')}, {first_match.get('lon', 'N/A')})")
        else:
            print("INFO: Nominatim Service returned no results or an unexpected format.")
            
    except Exception as e:
        print(f"FAIL: Nominatim Service Failed due to Exception: {e}")