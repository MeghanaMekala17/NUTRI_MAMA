# import requests
# import os

# PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# BASE_URL = "https://api.pexels.com/v1/search"

# def get_images(query: str):
#     headers = {"Authorization": PEXELS_API_KEY}
#     params = {"query": query, "per_page": 5}
#     response = requests.get(BASE_URL, headers=headers, params=params)

#     if response.status_code != 200:
#         return {"error": "Pexels request failed"}

#     return response.json()
import requests
import os

# ⚠️ WARNING: Hardcoding API keys like this is INSECURE for shared or production code.
# Use environment variables or a secure secret manager instead.
PEXELS_API_KEY = "YOUR_KEY"  # Replace this with your key

BASE_URL = "https://api.pexels.com/v1/search"

def get_images(query: str):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 5}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        # Include the status code and text for better error diagnosis
        return {
            "error": "Pexels request failed", 
            "status_code": response.status_code,
            "response_text": response.text
        }

    return response.json()

# --- Example Usage (Check Code) ---
if __name__ == '__main__':
    search_term = "nature"
    print(f"Searching for images of: '{search_term}'...")
    
    # 1. Call the function
    image_data = get_images(search_term)

    # 2. Check for errors
    if "error" in image_data:
        print("\n--- ERROR ---")
        print(f"Error: {image_data.get('error')}")
        print(f"Status Code: {image_data.get('status_code')}")
        # print(f"Response Text: {image_data.get('response_text')}") # Uncomment to see the raw error response
    else:
        # 3. Process and print results
        print("\n--- SUCCESS ---")
        total_results = image_data.get('total_results', 0)
        photos = image_data.get('photos', [])
        
        print(f"Total results found: {total_results}")
        print(f"Displayed photos: {len(photos)}")
        
        # Print details for each returned photo
        for i, photo in enumerate(photos):
            print(f"\nPhoto {i+1}:")
            print(f"  Photographer: {photo.get('photographer')}")
            print(f"  Alt Text: {photo.get('alt')}")
            # Print a specific image size URL (e.g., 'original' or 'tiny')
            print(f"  Original URL: {photo.get('src', {}).get('original', 'N/A')}")
