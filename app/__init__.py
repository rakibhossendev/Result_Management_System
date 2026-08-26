from flask import Flask
from .config import Config
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .routes.student.home import home_bp
    from .routes.auth.login import login_bp
    from .routes.admin.admin_dashboard import admin_bp
    from .routes.admin.add_principal import add_principal_bp
    from .routes.principal.principal_dashboard import principal_dashboard_bp
    from .routes.principal.add_teacher import add_teacher_bp
    from .routes.principal.view_teachers import views_teacher_bp
    from .routes.principal.teacher_details import teacher_details_bp
    from .routes.principal.edit_teacher import edit_teacher_bp
    from .routes.principal.subject_and_department.assign_subjects import assign_subject_bp
    from .routes.principal.subject_and_department.assign_subject_dashboard import assign_subject_dashboard_bp
    from .routes.principal.subject_and_department.show_subjects import show_subjects_bp
    from .routes.principal.subject_and_department.assign_teacher import assign_teacher_bp
    from .routes.principal.subject_and_department.get_subject import get_subject_bp
    from .routes.teacher.teacher_dashboard import teacher_dashboard_bp
    from .routes.teacher.add_student import add_student_bp
    from .routes.teacher.show_student import show_student_bp
    from .routes.teacher.edit_student import edit_student_bp
    from .routes.teacher.attendance import attendance_bp
    from .routes.teacher.get_marks_system.get_marks import get_marks_bp
    from .routes.teacher.get_marks_system.get_marks_dashboard import get_marks_dashboard_bp
    from .routes.teacher.get_marks_system.view_details import view_student_details_bp
    from .routes.teacher.get_marks_system.add_marks import add_marks_bp
    from .routes.teacher.get_marks_system.marks_deatils import marks_details_bp
    from .routes.teacher.get_marks_system.get_marks_topic import get_marks_topic_bp
    from .routes.student.student_dashboard import student_dashboard_bp
    from .routes.student.marks_details import subjects_marks_bp
    from .routes.student.attendance import student_attendance_bp
    from .routes.admin.upload_cgpa import upload_cgpa_bp
    from .routes.student.view_cgpa import view_student_cgpa_bp
    # API
    from .routes.api.student_data import student_data_api
    # AI
    from .routes.ai.routes import ai_bp
    # change password
    from app.routes.admin.change_password import admin_change_password_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(add_principal_bp)
    app.register_blueprint(principal_dashboard_bp)
    app.register_blueprint(add_teacher_bp)
    app.register_blueprint(views_teacher_bp)
    app.register_blueprint(teacher_details_bp)
    app.register_blueprint(edit_teacher_bp)
    app.register_blueprint(assign_subject_bp)
    app.register_blueprint(assign_subject_dashboard_bp)
    app.register_blueprint(show_subjects_bp)
    app.register_blueprint(assign_teacher_bp)
    app.register_blueprint(get_subject_bp)
    app.register_blueprint(teacher_dashboard_bp)
    app.register_blueprint(add_student_bp)
    app.register_blueprint(show_student_bp)
    app.register_blueprint(edit_student_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(get_marks_dashboard_bp)
    app.register_blueprint(get_marks_bp)
    app.register_blueprint(view_student_details_bp)
    app.register_blueprint(add_marks_bp)
    app.register_blueprint(marks_details_bp)
    app.register_blueprint(get_marks_topic_bp)
    app.register_blueprint(student_dashboard_bp)
    app.register_blueprint(subjects_marks_bp)
    app.register_blueprint(student_attendance_bp)
    app.register_blueprint(upload_cgpa_bp)
    app.register_blueprint(view_student_cgpa_bp)
    # Register API and AI blueprints
    app.register_blueprint(student_data_api)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_change_password_bp) # change password bp

    return app