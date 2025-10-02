import requests

# 🔑 Put your API key directly here
IPINFO_TOKEN = "YOUR_KEY"

BASE_URL = "https://ipinfo.io/"

def get_ip_details(ip: str = ""):
    url = f"{BASE_URL}{ip}?token={IPINFO_TOKEN}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "IPinfo request failed"}

    return response.json()


if __name__ == "__main__":
    # Test with your own IP or leave empty for auto-detection
    print(get_ip_details())
