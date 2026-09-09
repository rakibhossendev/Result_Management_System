
import os

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from app.extensions import db
from app.models.cgpa_upload import CGPAImportFile


view_pdf_bp = Blueprint(
    "view_pdf",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# VIEW UPLOADED PDF FILES
# =========================================================

@view_pdf_bp.route("/cgpa-pdfs")
def view_cgpa_pdfs():

    files = (
        CGPAImportFile.query
        .order_by(
            CGPAImportFile.id.desc()
        )
        .all()
    )

    return render_template(
        "admin/upload/view_pdf_file.html",
        files=files
    )


# =========================================================
# DELETE PDF FILE
# =========================================================

@view_pdf_bp.route(
    "/cgpa-pdfs/delete/<int:file_id>",
    methods=["POST"]
)
def delete_cgpa_pdf(file_id):

    file_record = (
        CGPAImportFile.query.get_or_404(file_id)
    )

    filename = file_record.filename

    pdf_path = os.path.join(
        current_app.instance_path,
        "cgpa_pdfs",
        filename
    )

    # Delete physical PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # Delete database record
    db.session.delete(file_record)
    db.session.commit()

    flash(
        f"{filename} deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "view_pdf.view_cgpa_pdfs"
        )
    )

