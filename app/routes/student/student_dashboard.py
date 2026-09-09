from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from app.models.teacher import AddStudentInfo
from app.routes.student.auth_check import student_roll_check


student_dashboard_bp = Blueprint(
    "student_dashboard",
    __name__,
    url_prefix="/student_dashboard"
)


@student_dashboard_bp.route("/")
def student_dashboard():

    # Student login check
    student_roll_check()

    # Session থেকে student ID
    student_id = session.get("student_id")

    if not student_id:
        flash("Please login first.", "danger")
        return redirect(url_for("home.home"))

    # Student information
    student_data = AddStudentInfo.query.filter_by(
        student_id=student_id
    ).first()

    if not student_data:
        flash("Student information not found.", "danger")
        return redirect(url_for("home.home"))

    return render_template(
        "student/student_dashboard.html",
        student_data=student_data
    )