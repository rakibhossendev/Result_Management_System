from flask import (
    Blueprint,
    render_template,
    session,
    request
)

from sqlalchemy import func

from app.routes.student.auth_check import student_roll_check
from app.models.teacher import Attendance, AddStudentInfo
from app.models.assign import Subjects, Curriculum
from app.extensions import db

student_attendance_bp = Blueprint(
    "student_attendance",
    __name__,
    url_prefix="/student_attendance"
)

# ============================================================
# Student Attendance
# ============================================================

@student_attendance_bp.route("/")
def attendance():

    # --------------------------------------------------------
    # Student Authentication
    # --------------------------------------------------------
    student_roll_check()

    student_id = session.get("student_id")

    if not student_id:
        return render_template(
            "student/attendance.html",
            attendance=None,
            subjects=[],
            selected_subject_id=None,
            total_class=0,
            total_present=0,
            total_absent=0,
            percentage=0
        )

    # ========================================================
    # Get Student Information
    # ========================================================
    student = AddStudentInfo.query.filter_by(
        student_id=student_id
    ).first()

    if not student:

        return render_template(
            "student/attendance.html",
            attendance=None,
            subjects=[],
            selected_subject_id=None,
            total_class=0,
            total_present=0,
            total_absent=0,
            percentage=0
        )

    # ========================================================
    # Get Student Subjects
    #
    # Subject comes from Curriculum:
    # department_id + semester
    # ========================================================
    curriculum_records = Curriculum.query.filter_by(
        department_id=student.department_id,
        semester=student.semester
    ).all()

    subjects = [
        curriculum.subject
        for curriculum in curriculum_records
        if curriculum.subject
    ]

    # ========================================================
    # Selected Subject
    # ========================================================
    selected_subject_id = request.args.get(
        "subject_id",
        type=int
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    attendance = None

    total_class = 0
    total_present = 0
    total_absent = 0
    percentage = 0

    # ========================================================
    # If Subject Selected
    # ========================================================
    if selected_subject_id:

        # ----------------------------------------------------
        # Security Check
        #
        # Selected subject MUST belong to this student's
        # department + semester curriculum.
        # ----------------------------------------------------
        valid_subject = Curriculum.query.filter_by(
            department_id=student.department_id,
            semester=student.semester,
            subject_id=selected_subject_id
        ).first()

        if valid_subject:

            # =================================================
            # Attendance Records
            # =================================================
            attendance = (
                Attendance.query
                .filter_by(
                    student_id=student_id,
                    subject_id=selected_subject_id
                )
                .order_by(
                    Attendance.attendance_date.desc()
                )
                .paginate(
                    page=page,
                    per_page=15,
                    error_out=False
                )
            )

            # =================================================
            # Total Class
            # =================================================
            total_class = (
                db.session.query(
                    func.count(Attendance.attendance_id)
                )
                .filter_by(
                    student_id=student_id,
                    subject_id=selected_subject_id
                )
                .scalar()
            ) or 0

            # =================================================
            # Total Present
            # =================================================
            total_present = (
                db.session.query(
                    func.count(Attendance.attendance_id)
                )
                .filter_by(
                    student_id=student_id,
                    subject_id=selected_subject_id,
                    status="P"
                )
                .scalar()
            ) or 0

            # =================================================
            # Total Absent
            # =================================================
            total_absent = (
                db.session.query(
                    func.count(Attendance.attendance_id)
                )
                .filter_by(
                    student_id=student_id,
                    subject_id=selected_subject_id,
                    status="A"
                )
                .scalar()
            ) or 0

            # =================================================
            # Attendance Percentage
            # =================================================
            if total_class > 0:

                percentage = round(
                    (total_present / total_class) * 100,
                    2
                )

        else:

            # Invalid subject for this student
            selected_subject_id = None

    # ========================================================
    # Render
    # ========================================================
    return render_template(
        "student/attendance.html",
        attendance=attendance,
        subjects=subjects,
        selected_subject_id=selected_subject_id,
        total_class=total_class,
        total_present=total_present,
        total_absent=total_absent,
        percentage=percentage
    )