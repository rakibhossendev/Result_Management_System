from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from app.models.teacher import AddStudentInfo
from app.models.cgpa_upload import StudentCGPA
from app.models.assign import Subjects

from app.routes.student.auth_check import student_roll_check


view_cgpa_bp = Blueprint(
    "view_cgpa",
    __name__,
    url_prefix="/student"
)


# =========================================================
# VIEW CGPA
# =========================================================

@view_cgpa_bp.route("/view-cgpa")
def view_cgpa():

    # -----------------------------------------------------
    # Student login check
    # -----------------------------------------------------

    student_roll_check()

    # -----------------------------------------------------
    # Session থেকে student ID
    # -----------------------------------------------------

    student_id = session.get("student_id")

    if not student_id:

        flash(
            "Please login first.",
            "danger"
        )

        return redirect(
            url_for("home.home")
        )

    # -----------------------------------------------------
    # student_data table থেকে student information
    # -----------------------------------------------------

    student_info = (
        AddStudentInfo.query
        .filter_by(student_id=student_id)
        .first()
    )

    if not student_info:

        flash(
            "Student information not found.",
            "danger"
        )

        return redirect(
            url_for("home.home")
        )

    # -----------------------------------------------------
    # Student roll
    # -----------------------------------------------------

    roll = str(student_info.student_roll)

    # -----------------------------------------------------
    # StudentCGPA table থেকে CGPA data
    # -----------------------------------------------------

    student = (
        StudentCGPA.query
        .filter_by(roll=roll)
        .first()
    )

    # -----------------------------------------------------
    # CGPA data না থাকলে
    # -----------------------------------------------------

    if not student:

        flash(
            "CGPA information is not available yet.",
            "warning"
        )

        return render_template(
            "student/view_cgpa.html",
            student=None,
            student_info=student_info,
            failed_subjects=[]
        )

    # -----------------------------------------------------
    # Failed subjects
    # -----------------------------------------------------

    failed_subjects = []

    if student.failed_subjects:

        failed_data = (
            student.failed_subjects
            .split(",")
        )

        for item in failed_data:

            item = item.strip()

            if not item:
                continue

            try:

                subject_code, subject_type = (
                    item.split(":", 1)
                )

            except ValueError:
                continue

            subject_code = subject_code.strip()
            subject_type = subject_type.strip()

            # -------------------------------------------------
            # Subject table থেকে subject information
            # -------------------------------------------------

            subject = (
                Subjects.query
                .filter_by(
                    subject_code=subject_code
                )
                .first()
            )

            failed_subjects.append({

                "code": subject_code,

                "type": subject_type,

                "name": (
                    subject.subject_name
                    if subject
                    else "Unknown Subject"
                )
            })

    # -----------------------------------------------------
    # Template
    # -----------------------------------------------------

    return render_template(
        "student/view_cgpa.html",
        student=student,
        student_info=student_info,
        failed_subjects=failed_subjects
    )