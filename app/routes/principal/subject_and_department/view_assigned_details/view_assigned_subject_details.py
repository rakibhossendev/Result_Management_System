from flask import Blueprint, render_template, session, url_for, redirect
from app.extensions import db
from app.models.assign import Subjects, TeacherAssignment

view_assigned_bp = Blueprint(
    "view_assigned",
    __name__,
    url_prefix="/view-assigned"
)


@view_assigned_bp.route("/")
def view_assigned():
     
    if not session.get("principal"):
        return redirect(url_for("login.login"))

    subjects = (
        db.session.query(Subjects)
        .order_by(Subjects.subject_id.desc())
        .all()
    )

    return render_template(
        "/principal/subject_and_department/view_assigned_details/view_assigned_subject_details.html",
        subjects=subjects
    )



@view_assigned_bp.route("/teacher/<int:subject_id>")
def view_teachers(subject_id):
    if not session.get("principal"):
        return redirect(url_for("login.login"))
    assignments = (
        db.session.query(TeacherAssignment).filter(
            TeacherAssignment.subject_id == subject_id
        ).all()
    )

    return render_template(
        "/principal/subject_and_department/view_assigned_details/view_assigned_teachers.html",
        assignments=assignments
    )


@view_assigned_bp.route(
    "/teacher/delete/<int:assignment_id>",
    methods=["POST"]
)
def delete_teacher_assignment(assignment_id):

    # if not session.get("principle"):
    #     return redirect(url_for("login.login"))

    assignment = (
        db.session.query(TeacherAssignment)
        .filter(
            TeacherAssignment.assignment_id == assignment_id
        )
        .first_or_404()
    )

    subject_id = assignment.subject_id

    db.session.delete(assignment)
    db.session.commit()

    return redirect(
        url_for(
            "view_assigned.view_teachers",
            subject_id=subject_id
        )
    )