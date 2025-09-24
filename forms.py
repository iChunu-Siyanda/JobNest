from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=250)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=250)])
    submit_login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=250)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=250)])
    submit_reg = SubmitField('Register')

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
