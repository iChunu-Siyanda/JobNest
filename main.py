import os
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")
bootstrap = Bootstrap5(app)

# API Config (from environment)
API_ID = os.getenv("ADZUNA_API_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/za/search/1"


#  Forms
class JobSearchForm(FlaskForm):
    job_search = StringField('Search Job', validators=[DataRequired()])
    loc_search = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Find Job')


class CompanySearchForm(FlaskForm):
    company_search = StringField('Search Company', validators=[DataRequired()])
    submit_company = SubmitField('Find Company')


class SalarySearchForm(FlaskForm):
    job_salary = StringField('Search Job', validators=[DataRequired()])
    loc_salary = StringField('Location', validators=[DataRequired()])
    submit_query = SubmitField('Get Salary')


# Fetch jobs
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

# ---------------- Routes ---------------- #
@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = JobSearchForm()
    if form.validate_on_submit():
        job = form.job_search.data
        location = form.loc_search.data
        return redirect(url_for("job_search", job=job, location=location))
    return render_template('index.html', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
def job_search():
    form = JobSearchForm()
    job = request.args.get("job", "")
    location = request.args.get("location", "")

    jobs = []
    if job and location:
        jobs = fetch_jobs(job, location)

    if form.validate_on_submit():
        job = form.job_search.data
        location = form.loc_search.data
        return redirect(url_for("job_search", job=job, location=location))

    return render_template("jobs.html", form=form, job=job, location=location, jobs=jobs)


@app.route('/company', methods=['GET', 'POST'])
def company_search():
    form = CompanySearchForm()
    if form.validate_on_submit():
        company = form.company_search.data
        # Future: hook company search to API
        return f"Results for {company}"

    companies = [
        {"title": "Software Engineer", "company": "Google", "location": "Johannesburg"},
        {"title": "Data Scientist", "company": "Amazon", "location": "Cape Town"},
        {"title": "Frontend Developer", "company": "Meta", "location": "Durban"},
        {"title": "Backend Developer", "company": "Netflix", "location": "Pretoria"},
        {"title": "Cloud Engineer", "company": "Microsoft", "location": "Johannesburg"},
    ]
    return render_template('company.html', form=form, companies=companies)


@app.route('/salary', methods=['GET', 'POST'])
def salaries_search():
    form = SalarySearchForm()
    salaries = []
    if form.validate_on_submit():
        job = form.job_salary.data
        location = form.loc_salary.data
        # Future: hook salary endpoint of Adzuna API
        return f"Salary results for {job} in {location}"
    return render_template('salaries.html', form=form, salaries=salaries)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
