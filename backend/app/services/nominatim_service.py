# import requests

# BASE_URL = "https://nominatim.openstreetmap.org/search"

# def get_location(query: str):
#     params = {"q": query, "format": "json"}
#     response = requests.get(BASE_URL, params=params)

#     if response.status_code != 200:
#         return {"error": "Nominatim request failed"}

#     return response.json()


import requests

def get_location(query: str):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json"},
        headers={"User-Agent": "TestApp/1.0"}
    )
    return response.json()

if __name__ == "__main__":
    result = get_location("Bangalore")
    if result:
        first = result[0]
        print("Location:", first["display_name"])
        print("Latitude:", first["lat"])
        print("Longitude:", first["lon"])
    else:
        print("No results found")
