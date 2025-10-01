import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_jobs(keyword, location, results_per_page=6):
    app_id = os.getenv("ADZUNA_API_ID")
    app_key = os.getenv("ADZUNA_API_KEY")

    if not app_id or not app_key:
        return []

    url = f"https://api.adzuna.com/v1/api/jobs/za/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": keyword,
        "where": location,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()

    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "title": item.get("title"),
            "company": item.get("company", {}).get("display_name", "N/A"),
            "location": item.get("location", {}).get("display_name", "N/A"),
            "redirect_url": item.get("redirect_url", "#")
        })

    return jobs
