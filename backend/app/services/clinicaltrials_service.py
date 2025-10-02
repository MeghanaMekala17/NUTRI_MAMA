import requests

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def get_trials(condition: str, page_size: int = 10):
    params = {
        "query.cond": condition,
        "pageSize": page_size,
        "countTotal": "true"
    }
    headers = {"User-Agent": "TestApp/1.0"}  # Optional but recommended
    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        return {
            "error": "ClinicalTrials.gov API request failed",
            "status_code": response.status_code,
            "message": response.text
        }

    return response.json()

if __name__ == "__main__":
    condition = "diabetes"
    output = get_trials(condition)
    print(output)
