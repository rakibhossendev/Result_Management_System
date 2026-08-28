from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)

from app.extensions import db
from app.models.assign import Department
from app.models.teacher import AddStudentInfo, Attendance
from app.utils.attendance_form import AttendanceForm
from app.routes.reuse_code import expetion_message

attendance_bp = Blueprint(
    "attendence",
    __name__,
    url_prefix="/attendance"
)


@attendance_bp.route("/", methods=["GET", "POST"])
def attendance():

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    form = AttendanceForm()

    teacher_id = session.get("teacher_id")
    principal_id = session.get("temp_principal_id")

    departments = Department.query.filter_by(
        principal_id=principal_id
    ).all()

    form.department_id.choices = [
        (
            d.department_id,
            f"{d.department_code} - {d.department_name}"
        )
        for d in departments
    ]

    students = AddStudentInfo.query.filter_by(
        teacher_id=teacher_id
    ).all()

    form.semester.choices = [
        (s, f"Semester {s}")
        for s in sorted({x.semester for x in students})
    ]

    form.group.choices = [
        (g, g)
        for g in sorted({x.group for x in students if x.group})
    ]

    student_data = []

    # Existing attendance status
    saved_attendance = {}

    try:

        if form.validate_on_submit():

            # Selected students
            student_data = AddStudentInfo.query.filter_by(
                teacher_id=teacher_id,
                department_id=form.department_id.data,
                semester=form.semester.data,
                group=form.group.data
            ).order_by(
                AddStudentInfo.student_roll
            ).all()

            # Get attendance for selected date
            attendance_records = Attendance.query.filter(
                Attendance.attendance_date == form.attendance_date.data,
                Attendance.student_id.in_(
                    [student.student_id for student in student_data]
                )
            ).all()

            # Create dictionary:
            # {student_id: "P/A"}
            saved_attendance = {
                record.student_id: record.status
                for record in attendance_records
            }

    except Exception:

        db.session.rollback()

        flash("Something Wrong", "danger")

    return render_template(
        "teacher/attendance.html",
        form=form,
        students=student_data,
        saved_attendance=saved_attendance
    )


@attendance_bp.route("/save", methods=["POST"])
def save_attendance():

    if not session.get("teacher"):
        return redirect(url_for("login.login"))

    teacher_id = session.get("teacher_id")

    attendance_date = datetime.strptime(
        request.form.get("attendance_date"),
        "%Y-%m-%d"
    ).date()

    department_id = int(request.form.get("department_id"))
    semester = int(request.form.get("semester"))
    group = request.form.get("group")

    students = AddStudentInfo.query.filter_by(
        teacher_id=teacher_id,
        department_id=department_id,
        semester=semester,
        group=group
    ).all()

    for student in students:

        status = request.form.get(
            f"attendance_{student.student_id}"
        )

        old_attendance = Attendance.query.filter_by(
            student_id=student.student_id,
            attendance_date=attendance_date
        ).first()

        if old_attendance:

            old_attendance.status = status

        else:

            attendance = Attendance(
                student_id=student.student_id,
                teacher_id=teacher_id,
                attendance_date=attendance_date,
                status=status
            )

            db.session.add(attendance)

    db.session.commit()

    flash("Attendance Saved Successfully", "success")

    return redirect(url_for("attendence.attendance"))