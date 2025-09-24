from flask import Blueprint, render_template, request, redirect, url_for

salaries_bp = Blueprint("salaries", __name__, url_prefix="/salaries")

class SalarySearchForm(FlaskForm):
    job_salary = StringField('Search Job', validators=[DataRequired()])
    loc_salary = StringField('Location', validators=[DataRequired()])
    submit_query = SubmitField('Get Salary')

@salaries_bp.route('/salaries', methods=['GET', 'POST'])
def salaries_search():
    form = SalarySearchForm()
    salaries = []
    if form.validate_on_submit():
        job = form.job_salary.data
        location = form.loc_salary.data
        # Future: hook salary endpoint of Adzuna API
        return f"Salary results for {job} in {location}"
    return render_template('salaries.html', form=form, salaries=salaries)