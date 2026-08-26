from flask import Blueprint, redirect, url_for, session, render_template,flash
from app.models.principal import TeacherAddInfo
from app.utils.principalForm import AddTeacherForm
from app.extensions import db
from werkzeug.security import generate_password_hash

edit_teacher_bp = Blueprint(
    "edit_teacher",
    __name__,
    url_prefix="/edit_teacher"
)

@edit_teacher_bp.route("/")
def edit_teacher_view():
    if not session.get("principal"):
        return redirect(url_for("login.login"))

    principal_id = session.get("principal_id")
    teachers_data = TeacherAddInfo.query.filter_by(
        principal_id=principal_id
    ).all()

    return render_template(
        "principal/edit_teacher_view.html",
        teachers_data=teachers_data
    )


@edit_teacher_bp.route("/principal/<int:teacher_id>/edit",methods=["GET","POST"])
def edit_teacher(teacher_id):
       
    if not session.get("principal"):
        return redirect(url_for("login.login"))
        
    teacher =TeacherAddInfo.query.get_or_404(teacher_id)
    form = AddTeacherForm(obj=teacher)

    try:
        if form.validate_on_submit():

            teacher.teacher_id = form.teacher_id.data
            teacher.first_name = form.first_name.data
            teacher.last_name = form.last_name.data
            teacher.institute = form.institute.data 
            teacher.institute_code = form.institute_code.data
            teacher.phone = form.phone.data
            teacher.email = form.email.data
            teacher.username = form.username.data
            teacher.password_hash = generate_password_hash(form.password.data)

            db.session.commit()
            flash("Teacher data edited!","success")
            return redirect(url_for("principal_dashboard.principal_dashboard"))
    except Exception as e:
        db.session.rollback()
        flash("wrong","danger")

    return render_template(
        "principal/edit_teacher.html",
        form = form,
        teacher = teacher
    )


@edit_teacher_bp.route("/principal/<int:teacher_id>/delete", methods=["POST"])
def delete_teacher(teacher_id):
    teacher = TeacherAddInfo.query.get_or_404(teacher_id)

    try:
        db.session.delete(teacher)   
        db.session.commit()
        flash("Teacher deleted successfully", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting teacher: {str(e)}", "danger")

    return redirect(url_for('principal_dashboard.principal_dashboard'))