from flask import Blueprint, render_template, request, redirect, url_for
from apis import fetch_jobs
from forms import JobSearchForm

# Blueprint registered at /jobs
jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

@jobs_bp.route("/", methods=["GET", "POST"])
def job_search():
    form = JobSearchForm()
    job = request.args.get("job", "")
    location = request.args.get("location", "")

    jobs = []
    if job and location:
        jobs = fetch_jobs(keyword=job, location=location)

    if form.validate_on_submit():
        job = form.job_search.data
        location = form.loc_search.data
        return redirect(url_for("jobs.job_search", job=job, location=location))

    return render_template(
        "jobs.html",
        form=form,
        job=job,
        location=location,
        jobs=jobs
    )
