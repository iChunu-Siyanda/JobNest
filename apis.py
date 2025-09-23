from dotenv import load_dotenv
import os
import requests

#============= API Config (from environment) ============
load_dotenv()

API_ID = os.getenv("ADZUNA_API_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/za/search/1"


#===================== Fetch jobs ========================
def fetch_jobs(job_title, location):
    """Call Adzuna API and return job listings with clean strings."""
    params = {
        "app_id": API_ID,
        "app_key": API_KEY,
        "results_per_page": 10,
        "what": job_title,
        "where": location,
        "sort_by": "date"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data.get("results", []):
                company_raw = job.get("company", {})
                location_raw = job.get("location", {})

                jobs.append({
                    "title": job.get("title") or "No title provided",
                    "company": company_raw.get("display_name") if isinstance(company_raw, dict) else company_raw or "Unknown company",
                    "location": location_raw.get("display_name") if isinstance(location_raw, dict) else location_raw or "Location not specified",
                    "url": job.get("redirect_url") or "#"
                })
            return jobs
        else:
            print("API Error:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching jobs:", e)
        return []
