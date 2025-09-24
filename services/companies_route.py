from flask import Blueprint, render_template, request, redirect, url_for
from forms import CompanySearchForm

companies_bp = Blueprint("companies", __name__, url_prefix="/companies")

@companies_bp.route('/company', methods=['GET', 'POST'])
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