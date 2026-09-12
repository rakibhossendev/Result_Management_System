from flask import Blueprint, jsonify
from app.models.teacher import AddStudentInfo


student_data_api_bp = Blueprint(
    "student_data_api",
    __name__,
    url_prefix="/student/data/api"
)


@student_data_api_bp.route("/<int:student_roll>", methods=["GET"])
def student_data_api(student_roll):

    student = AddStudentInfo.query.filter_by(
        student_roll=student_roll
    ).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student Not Found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Student is Found",
        "data": {
            "student_id": student.student_id,
            "student_roll": student.student_roll,
            "student_name": student.student_full_name,
            "semester": student.semester,
            "group": student.group,
            "cgpa": student.cgpa
        }
    }), 200