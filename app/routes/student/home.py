from flask import Blueprint, render_template,flash,redirect,url_for,session
from app.utils.form import SearchForm
from app.models.teacher import AddStudentInfo

home_bp = Blueprint('home', __name__,url_prefix="/")
@home_bp.route("/", methods=["GET", "POST"])
def home():
    search = SearchForm()
    student_data = AddStudentInfo.query.filter_by()
    if search.validate_on_submit():
        student_roll = search.roll.data
        student = AddStudentInfo.query.filter_by(student_roll=student_roll).first()
        if student:
            session["student"] = True
            session["student_id"] = student.student_id
            flash(f"Welcome To {student.student_full_name}","success")
            return redirect(url_for("student_dashboard.student_dashboard"))
        else:
            flash("Invalid Roll","danger")
            return redirect(url_for("home.home"))
        
    return render_template(
        "home/home.html", 
        search=search
    )

