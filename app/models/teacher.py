from app.extensions import db
from datetime import datetime

class AddStudentInfo(db.Model):
    __tablename__ = "student_data"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_roll = db.Column(db.Integer, unique=True, nullable=False)
    student_full_name = db.Column(db.String(250), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    group = db.Column(db.String(1))
    cgpa = db.Column(db.Float, default=0)
    department_id = db.Column(db.Integer,db.ForeignKey("departments.department_id"),nullable=False)
    principal_id = db.Column(db.Integer,db.ForeignKey("principal_info.principal_id"))
    teacher_id = db.Column(db.Integer,db.ForeignKey("teacher_info.teacher_id"))

class Attendance(db.Model):
    __tablename__ = "attendance"

    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_data.student_id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_info.teacher_id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.subject_id"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    student = db.relationship("AddStudentInfo", backref="attendance")
    subject = db.relationship("Subjects", backref="attendance")

    __table_args__ = (db.UniqueConstraint("student_id", "subject_id", "attendance_date", name="unique_student_subject_attendance"),)

    
class MarksTopic(db.Model):
    __tablename__ = "marks_topic"
    marks_topic_id = db.Column(db.Integer,primary_key=True)
    marks_topic_name = db.Column(db.String(100),nullable=False)
    full_marks = db.Column(db.Integer,nullable=False,)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.subject_id"),nullable=False)
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_info.teacher_id"),
        nullable=False
    )

class AddMarks(db.Model):
    __tablename__ = "add_marks"

    marks_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_data.student_id"),nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.subject_id"),nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_info.teacher_id"),nullable=False)
    marks_topic_id = db.Column(db.Integer, db.ForeignKey("marks_topic.marks_topic_id"),nullable=False)
    obtained_marks = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    student = db.relationship("AddStudentInfo", backref="marks")
    subject = db.relationship("Subjects", backref="marks")
    topic = db.relationship("MarksTopic", backref="marks")

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "subject_id",
            "marks_topic_id",
            name="unique_student_subject_topic"
        ),
    )