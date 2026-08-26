from flask import Blueprint,redirect,url_for,session,render_template,flash
from werkzeug.security import generate_password_hash,check_password_hash
from app.models.admin import Admin
from app.utils.change_password import ChangePasswordForm
from app.extensions import db

admin_change_password_bp = Blueprint(
    "admin_change_password",
    __name__,
    url_prefix="/admin_change_password"
)

@admin_change_password_bp.route("", methods=["GET","POST"])
def change_password():
    if not session.get("admin"):
        return redirect(url_for("auth.login"))
    
    admin = db.session.get(Admin, session["admin_id"])
    form = ChangePasswordForm()

    if not admin:
        session.clear()
        flash("Admin account not found.", "danger")
        return redirect(url_for("auth.login"))
    
    try:
        if form.validate_on_submit():
            if check_password_hash(admin.password_hash,form.old_password.data):
                admin.username = form.username.data
                admin.password_hash = generate_password_hash(form.new_password.data)
                db.session.commit()
                flash("Admin Password or username saved successfully","success")
                return redirect(url_for("admin_dashboard.admin_dashboard"))
            else:
                flash("Old password is not match","danger")
                return redirect(url_for("admin_change_password.change_password"))
            
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}","danger")
        return redirect(url_for("admin_dashboard.admin_dashboard"))

    return render_template(
        "admin/change_password.html",
        form=form,
        admin=admin
    )
    




