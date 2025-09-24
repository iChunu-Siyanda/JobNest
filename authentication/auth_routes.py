from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from forms import LoginForm, RegisterForm
from models import Users

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        if Users.query.filter_by(username=form.username.data).first():
            flash("Username already taken!", "danger")
            return render_template("sign_up.html", form=form)

        # Hash the password
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")

        # Create and save new user
        new_user = Users(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("sign_up.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid username or password", "danger")
        return redirect(url_for("home_page"))
    return render_template("login.html", form=form)

# @auth_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("welcome_page"))
