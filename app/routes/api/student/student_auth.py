from flask import Blueprint,request,jsonify
from app.models.teacher import AddStudentInfo

search_student_bp = Blueprint(
    "/student_search",
    __name__,
    url_prefix="/api/student"
)

@search_student_bp.route("/search",methods=["POST"])
def search_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    student_roll = data.get("student_roll")

    if not student_roll:
        return jsonify({
            "success": False,
            "message": "Student Roll is not required"
        }),400

    try:
        student_roll = int(student_roll)
    except (ValueError,TypeError):
        return jsonify({
            "success": False,
            "message": "Student Roll Must be a number"
        })
    student = AddStudentInfo.query.filter_by(student_roll=student_roll).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not Found"
        }), 404
    
    return jsonify({
        "success": True,
        "message": "Student Found",
        "student": "student_id"
    })

