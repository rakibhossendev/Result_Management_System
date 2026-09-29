from flask import jsonify,Blueprint
from app.models.teacher import Attendance,AddStudentInfo

attendance_api_bp = Blueprint(
    "attendance_api",
    __name__,
    url_prefix="/attendance/api/"
)

@attendance_api_bp.route("/<int:student_roll>", methods=["GET"])
def attendance_api(student_roll):

    student = AddStudentInfo.query.filter_by(
        student_roll=student_roll
    ).first()

    if not student:
        return jsonify({
            "success": False,
            "message": f"Student with roll {student_roll} not found"
        }), 404

    attendance_data = (
        Attendance.query
        .filter_by(student_id=student.student_id)
        .order_by(Attendance.attendance_date.desc())
        .all()
    )

    data = [
        {
            "attendance_id": attendance.attendance_id,
            "subject_name": attendance.subject.subject_name,
            "attendance_date": attendance.attendance_date.isoformat(),
            "status": attendance.status,
        }
        for attendance in attendance_data
    ]

    return jsonify({
        "success": True,
        "student_roll": student_roll,
        "total": len(data),
        "data": data
    })