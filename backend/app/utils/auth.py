import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key(service_name: str) -> str:
    key = os.getenv(service_name.upper() + "_API_KEY")
    if not key:
        raise ValueError(f"API key for {service_name} not found in environment")
    return key
