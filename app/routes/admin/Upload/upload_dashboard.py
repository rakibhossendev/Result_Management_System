from flask import Blueprint,redirect,render_template,session,url_for

upload_dashboard_bp = Blueprint(
    "upload_dashboard",
    __name__,
    url_prefix="/upload_dashboard"
)

@upload_dashboard_bp.route("/",methods=["GET"])
def upload_dashboard():
    if not session.get("admin"):
        return redirect(url_for('login.login'))

    return render_template("admin/upload/upload_dashboard.html")