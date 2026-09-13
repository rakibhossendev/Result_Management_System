from flask import Blueprint,jsonify,session
from app.models.teacher import Attendance

def attendance():
    student_id = session.get("student_roll")

    data = Attendance.query.filter_by(student_roll=student_roll).all()

    