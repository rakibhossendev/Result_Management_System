"""
Agent tool functions for the Mistral-powered assistant.

Each function here is meant to eventually be exposed to the model as a
"tool" (function calling). For now they are plain Python functions we can
call and test directly before wiring up tool-call routing.

Convention used across these tools:
- Every function is scoped by teacher_id, matching the ownership pattern
  already used in app/routes/teacher/show_student.py (AddStudentInfo is
  queried by teacher_id, not principal_id).
- Every function returns a plain dict (JSON-serializable) or None if not
  found / not owned by this teacher. Never return raw SQLAlchemy model
  instances to the agent layer.
"""

from app.models.teacher import AddStudentInfo, Attendance, AddMarks, MarksTopic
from app.models.assign import Department, Subjects


def get_student_data(student_id, teacher_id):
    """
    Fetch a single student's profile by internal student_id,
    scoped to the requesting teacher.

    Args:
        student_id (int): AddStudentInfo.student_id (auto-increment PK).
        teacher_id (int): The teacher making the request (from session).

    Returns:
        dict | None: Student data, or None if not found for this teacher.
    """
    student = AddStudentInfo.query.filter_by(
        student_id=student_id,
        teacher_id=teacher_id
    ).first()

    if student is None:
        return None

    department = Department.query.filter_by(
        department_id=student.department_id
    ).first()

    return {
        "student_id": student.student_id,
        "student_roll": student.student_roll,
        "student_full_name": student.student_full_name,
        "semester": student.semester,
        "group": student.group,
        "cgpa": student.cgpa,
        "department_id": student.department_id,
        "department_name": department.department_name if department else None,
        "department_code": department.department_code if department else None,
        "teacher_id": student.teacher_id,
        "principal_id": student.principal_id,
    }


def get_student_by_roll(student_roll, teacher_id):
    """
    Fetch a single student's profile by roll number (the human-facing ID),
    scoped to the requesting teacher.

    Args:
        student_roll (int): AddStudentInfo.student_roll (unique, user-facing).
        teacher_id (int): The teacher making the request (from session).

    Returns:
        dict | None: Student data, or None if not found for this teacher.
    """
    student = AddStudentInfo.query.filter_by(
        student_roll=student_roll,
        teacher_id=teacher_id
    ).first()

    if student is None:
        return None

    department = Department.query.filter_by(
        department_id=student.department_id
    ).first()

    return {
        "student_id": student.student_id,
        "student_roll": student.student_roll,
        "student_full_name": student.student_full_name,
        "semester": student.semester,
        "group": student.group,
        "cgpa": student.cgpa,
        "department_id": student.department_id,
        "department_name": department.department_name if department else None,
        "department_code": department.department_code if department else None,
        "teacher_id": student.teacher_id,
        "principal_id": student.principal_id,
    }

def get_student_attendance(student_roll, teacher_id):
    """
    Fetch attendance records for a single student, scoped to the teacher.

    Args:
        student_roll (int): Student's roll number.
        teacher_id (int): Teacher making the request.

    Returns:
        dict: Contains student info and a list of attendance records,
              or error if student not found.
    """
    student = AddStudentInfo.query.filter_by(
        student_roll=student_roll,
        teacher_id=teacher_id
    ).first()

    if student is None:
        return {"error": "student not found"}

    attendance_records = Attendance.query.filter_by(
        student_id=student.student_id,
        teacher_id=teacher_id
    ).order_by(Attendance.attendance_date).all()

    records = [
        {
            "attendance_date": rec.attendance_date.isoformat(),
            "status": rec.status,
        }
        for rec in attendance_records
    ]

    return {
        "student_id": student.student_id,
        "student_roll": student.student_roll,
        "student_full_name": student.student_full_name,
        "attendance_records": records,
    }

def get_student_marks(student_roll, teacher_id):
    """
    Fetch all marks for a student, scoped to the teacher.

    Args:
        student_roll (int): Student's roll number.
        teacher_id (int): Teacher making the request.

    Returns:
        dict: Contains student info and a list of marks with subject/topic details.
    """
    student = AddStudentInfo.query.filter_by(
        student_roll=student_roll,
        teacher_id=teacher_id
    ).first()

    if student is None:
        return {"error": "student not found"}

    marks = AddMarks.query.filter_by(
        student_id=student.student_id,
        teacher_id=teacher_id
    ).all()

    marks_data = []
    for mark in marks:
        subject = Subjects.query.filter_by(subject_id=mark.subject_id).first()
        topic = MarksTopic.query.filter_by(marks_topic_id=mark.marks_topic_id).first()
        marks_data.append({
            "subject_name": subject.subject_name if subject else "Unknown",
            "subject_code": subject.subject_code if subject else "Unknown",
            "marks_topic_name": topic.marks_topic_name if topic else "Unknown",
            "full_marks": topic.full_marks if topic else None,
            "obtained_marks": mark.obtained_marks,
        })

    return {
        "student_id": student.student_id,
        "student_roll": student.student_roll,
        "student_full_name": student.student_full_name,
        "marks": marks_data,
    }

def get_class_attendance(semester, group, teacher_id):
    """
    Fetch attendance records for all students in a given semester and group,
    scoped to the teacher.

    Args:
        semester (int): Semester number.
        group (str): Group letter (single character, e.g., "A").
        teacher_id (int): Teacher making the request.

    Returns:
        dict: Contains class info and a list of students with attendance count,
              present count, and attendance percentage.
    """
    students = AddStudentInfo.query.filter_by(
        semester=semester,
        group=group,
        teacher_id=teacher_id
    ).all()

    if not students:
        return {"error": "no students found for this class"}

    class_data = []
    for student in students:
        attendance_records = Attendance.query.filter_by(
            student_id=student.student_id,
            teacher_id=teacher_id
        ).all()

        total_days = len(attendance_records)
        present_days = sum(1 for rec in attendance_records if rec.status == "P")
        attendance_percent = (present_days / total_days * 100) if total_days else 0

        class_data.append({
            "student_roll": student.student_roll,
            "student_full_name": student.student_full_name,
            "total_days": total_days,
            "present_days": present_days,
            "attendance_percentage": round(attendance_percent, 2),
        })

    return {
        "semester": semester,
        "group": group,
        "students": class_data,
    }

def get_class_marks_summary(semester, group, teacher_id):
    """
    Fetch marks summary for all students in a given semester and group,
    scoped to the teacher.

    Args:
        semester (int): Semester number.
        group (str): Group letter.
        teacher_id (int): Teacher making the request.

    Returns:
        dict: Contains class info and a list of subject-wise statistics.
    """
    students = AddStudentInfo.query.filter_by(
        semester=semester,
        group=group,
        teacher_id=teacher_id
    ).all()

    if not students:
        return {"error": "no students found for this class"}

    student_ids = [s.student_id for s in students]

    # Get all marks for these students, for this teacher
    marks = AddMarks.query.filter(
        AddMarks.student_id.in_(student_ids),
        AddMarks.teacher_id == teacher_id
    ).all()

    if not marks:
        return {"error": "no marks found for this class"}

    # Group by subject_id
    subject_marks = {}
    for mark in marks:
        subject = Subjects.query.filter_by(subject_id=mark.subject_id).first()
        subject_name = subject.subject_name if subject else "Unknown"
        if subject_name not in subject_marks:
            subject_marks[subject_name] = []
        subject_marks[subject_name].append(mark.obtained_marks)

    summary = []
    for subject_name, scores in subject_marks.items():
        summary.append({
            "subject": subject_name,
            "num_students": len(scores),
            "average_obtained": round(sum(scores) / len(scores), 2),
            "min_obtained": min(scores),
            "max_obtained": max(scores),
        })

    return {
        "semester": semester,
        "group": group,
        "subject_wise_summary": summary,
    }


if __name__ == "__main__":
    # Manual test harness. Run with:
    #   python -m app.ai.tools
    # (Requires an app context and an existing student/teacher in the DB —
    # adjust the ids below to match real rows in your database.db)
    from app import create_app  # adjust import to match your actual app factory

    app = create_app()
    with app.app_context():
        result = get_student_data(student_id=1, teacher_id=1)
        print(result)