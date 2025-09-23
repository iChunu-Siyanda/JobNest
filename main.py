from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from apis import fetch_jobs

#=============== Load environment variables ====================
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")
bootstrap = Bootstrap5(app)

# ================== Forms ============================
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


# ================= Routes ================ #
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
