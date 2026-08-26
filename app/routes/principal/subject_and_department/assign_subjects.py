from flask import Blueprint,redirect,url_for,render_template,flash,session
from app.utils.assign_form import CurriculamForm,SubjectForm,DepartmentForm
from app.extensions import db
from app.models.assign import Department,Subjects,Curriculum

assign_subject_bp = Blueprint(
    "assign_subject",
    __name__,
    url_prefix="/assign_subject"
)

@assign_subject_bp.route("/add_department", methods=["GET", "POST"])
def add_department():
    if not session.get("principal"):
        return redirect(url_for("login.login"))

    form = DepartmentForm()
    try:
        if form.validate_on_submit():

            principal_id = session.get("principal_id")

            department = Department(
                department_code=form.department_code.data,
                department_name=form.department_name.data,
                principal_id=principal_id
            )

            db.session.add(department)
            db.session.commit()

            flash("Department added successfully", "success")
            return redirect(
                url_for("assign_subject_dashboard.assign_subject_dashboard")
            )
    except Exception as e:
        flash("This department is alrady exist","danger")
        return redirect(url_for("assign_subject.add_department"))

    return render_template(
        "principal/subject_and_department/add_department.html",
        form=form
    )


@assign_subject_bp.route("/",methods=["GET","POST"])
def assign_subject():
    if not session.get("principal"):
        return redirect(url_for("login.login"))
    
    form = CurriculamForm()

    principal_id = session.get("principal_id")
    departments = Department.query.filter_by(
        principal_id=principal_id
    ).all()

    form.department_id.choices = [
        (
            (d.department_id, f"{d.department_code} - {d.department_name}")
        )

        for d in departments
    ]

    subjects = Subjects.query.filter_by(
        principal_id=principal_id
    ).all()

    form.subject_id.choices = [
        (
            subject.subject_id,
            f"{subject.subject_code} - {subject.subject_name}"
        )

        for subject in subjects
    ]

    if form.validate_on_submit():

        curriculam = Curriculum(
            department_id=form.department_id.data,
            semester = form.semester.data,
            subject_id = form.subject_id.data
        )

        db.session.add(curriculam)
        db.session.commit()

        flash("Subject Assigned","success")
        return redirect(url_for("assign_subject_dashboard.assign_subject_dashboard"))
    
    return render_template(
        "principal/subject_and_department/assign_subject.html",
        form=form
    )

@assign_subject_bp.route("/add_subject", methods=["GET", "POST"])
def add_subject():

    if not session.get("principal"):
        return redirect(url_for("login.login"))

    form = SubjectForm()
    
    try:
        if form.validate_on_submit():

            principal_id = session.get("principal_id")

            subject = Subjects(
                subject_code=form.subject_code.data,
                subject_name=form.subject_name.data,
                principal_id=principal_id
            )

            db.session.add(subject)
            db.session.commit()

            flash("subject added successfully", "success")
            return redirect(
                url_for("assign_subject_dashboard.assign_subject_dashboard")
            )
        
    except Exception as e:
        flash(f"Error adding Subject {str(e)}","danger")
        return redirect(url_for("assign_subject.add_subject"))

    return render_template(
        "principal/subject_and_department/add_subject.html",
        form=form
    )