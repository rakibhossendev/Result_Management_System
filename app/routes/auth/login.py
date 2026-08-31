from flask import Blueprint, redirect, render_template, url_for, flash, session
from app.utils.form import LoginForm
from app.models.admin import PrincipalDataInfo,Admin
from app.models.principal import TeacherAddInfo
from app.utils.form import ShiftSelectForm
from app.extensions import db
from werkzeug.security import check_password_hash,generate_password_hash

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    admin = Admin.query.first()

    try:
        if not admin:
            admin = Admin(
                username="admin",
                password_hash=generate_password_hash("admin123")
            )

            db.session.add(admin)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}","danger")

    
    try:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            admin = Admin.query.filter_by(username=username).first()
            if admin and check_password_hash(admin.password_hash, password):
                session.clear()
                session["admin"] = True
                session["admin_id"] = admin.id
                flash("Admin Login Successful","success")
                return redirect(url_for("admin_dashboard.admin_dashboard"))
    
            # Principal Login
            principal = PrincipalDataInfo.query.filter_by(username=username).first()
            if principal and check_password_hash(principal.password_hash,password):
                session.clear()
                session["principal"] = True
                session["temp_principal_id"] = principal.principal_id
                return redirect(url_for("login.select_shift"))

        # teacher login
            teacher = TeacherAddInfo.query.filter_by(username=username).first()
            if teacher and check_password_hash(teacher.password_hash, password):
                session.clear()
                session["teacher"] = True
                session["teacher_id"] = teacher.teacher_id
                session["temp_principal_id"] = teacher.principal_id
                flash("Login successfully", "success")

                return redirect(
                    url_for("teacher_dashboard.teacher_dashboard")
                )
    
    except Exception as e:
        db.session.rollback()   
        flash("Invalid username and password","danger")

    return render_template("auth/login.html",login_form=form)

@login_bp.route("/logout")
def logout():
    session.pop("admin", None)  
    flash("Logged out successfully!", "success")
    return redirect(url_for("home.home"))

@login_bp.route("/logout_principal")
def logout_principal():
    session.pop("principal",None)
    flash("logout Successfully","success")
    return redirect(url_for("login.login"))


@login_bp.route(
    "/select_shift",
    methods=["GET", "POST"]
)
def select_shift():

    if "temp_principal_id" not in session:
        return redirect(url_for("login.login"))

    form = ShiftSelectForm()
    if form.validate_on_submit():
        session["principal"] = True
        session["principal_id"] = session["temp_principal_id"]
        session["shift"] = form.shift.data
        session.pop("temp_principal_id",None)

        flash(f"{form.shift.data} Shift Selected","success")

        return redirect(url_for("principal_dashboard.principal_dashboard"))

    return render_template(
        "auth/select_shift.html",
        form=form
    )