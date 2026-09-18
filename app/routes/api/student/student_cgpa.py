from flask import Blueprint,jsonify
from app.models.cgpa_upload import StudentCGPA

student_cgpa_bp = Blueprint(
    "student_cgpa",
    url_prefix="api/student/student_cgpa"
)

@student_cgpa_bp.route("/",methods=["GET"])
def student_cgpa_api():
    student_cgpa = StudentCGPA.query.all()

    data = []

    