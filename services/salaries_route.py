from flask import Blueprint, render_template
from forms import SalarySearchForm

salaries_bp = Blueprint("salaries", __name__, url_prefix="/salaries")

@salaries_bp.route('/', methods=['GET', 'POST'])
def salaries_search():
    form = SalarySearchForm()
    salaries = []
    if form.validate_on_submit():
        job = form.job_salary.data
        location = form.loc_salary.data
        # Future: Adzuna API
        return f"Salary results for {job} in {location}"
    return render_template('salaries.html', form=form, salaries=salaries)