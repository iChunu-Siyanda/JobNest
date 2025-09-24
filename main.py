from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from extensions import db, login_manager, bootstrap

#blueprints
from authentication.auth_routes import auth_bp
from services.companies_route import companies_bp
from services.salaries_route import salaries_bp
from services.jobs_route import jobs_bp, JobSearchForm

load_dotenv()

app = Flask(__name__, instance_relative_config=True)

def create_app():
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'users.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    login_manager.login_view = "auth.login"

    # Flask-Migrate
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(salaries_bp)

    # Homepage
    @app.route('/', methods=['GET', 'POST'])
    def home_page():
        form = JobSearchForm()
        if form.validate_on_submit():
            job = form.job_search.data
            location = form.loc_search.data
            return redirect(url_for("job_search", job=job, location=location))
        return render_template('index.html', form=form)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
