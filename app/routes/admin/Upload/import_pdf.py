
import os
import re

import fitz  # PyMuPDF

from flask import (Blueprint,render_template,request,redirect,url_for,flash,current_app)
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app.extensions import db
from app.models.cgpa_upload import CGPAImportFile
from app.models.cgpa_upload import StudentCGPA


import_pdf_bp = Blueprint(
    "import_pdf",
    __name__,
    url_prefix="/admin"
)

ALLOWED_EXTENSIONS = {"pdf"}
# =========================================================
# REGEX - COMPILED ONCE
# =========================================================

ROLL_BLOCK_RE = re.compile(
    r"(\d{6})\s*(?:\{([^}]*)\}|\(([^)]*)\))",
    re.IGNORECASE
)

GPA_RE = re.compile(
    r"gpa([1-8])\s*:\s*(ref|\d+(?:\.\d+)?)",
    re.IGNORECASE
)

FAILED_SUBJECT_RE = re.compile(
    r"(\d{5,6})\s*\(\s*([TP])\s*\)",
    re.IGNORECASE
)

DIRECT_GPA_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s*$"
)


# =========================================================
# FILE CHECK
# =========================================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# =========================================================
# FAST PDF TEXT EXTRACTION
# PyMuPDF is much faster than pypdf for normal text PDFs
# =========================================================

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    try:
        return " ".join(
            page.get_text("text")
            for page in doc
        )
    finally:
        doc.close()


# =========================================================
# PARSER
# =========================================================

def parse_gpa_data(content):
    # Normalize whitespace once
    content = re.sub(r"\s+", " ", content)
    students = []
    for match in ROLL_BLOCK_RE.finditer(content):
        roll = match.group(1)
        body = (
            match.group(2)
            or match.group(3)
            or ""
        ).strip()
        gpas = {}

        # -------------------------------------------------
        # GPA
        # -------------------------------------------------

        for semester, value in GPA_RE.findall(body):
            semester = int(semester)
            if value.lower() == "ref":
                gpas[semester] = None
            else:
                gpas[semester] = float(value)

        # -------------------------------------------------
        # 1st semester direct GPA
        #
        # 224618 (3.95)
        # -------------------------------------------------

        if not gpas:
            direct = DIRECT_GPA_RE.fullmatch(body)
            if direct:
                gpas[1] = float(direct.group(1))

        # -------------------------------------------------
        # FAILED SUBJECTS
        #
        # 25913(T)
        # 26411(T)
        # -------------------------------------------------

        failed_matches = FAILED_SUBJECT_RE.findall(body)
        failed_subjects = [
            f"{code}:{subject_type.upper()}"
            for code, subject_type in failed_matches
        ]

        # -------------------------------------------------
        # Calculate CGPA
        # -------------------------------------------------

        valid_gpas = [
            value
            for value in gpas.values()
            if value is not None
        ]
        cgpa = (
            round(sum(valid_gpas) / len(valid_gpas), 2)
            if valid_gpas
            else None
        )
        students.append({
            "roll": roll,
            "gpa1": gpas.get(1),
            "gpa2": gpas.get(2),
            "gpa3": gpas.get(3),
            "gpa4": gpas.get(4),
            "gpa5": gpas.get(5),
            "gpa6": gpas.get(6),
            "gpa7": gpas.get(7),
            "gpa8": gpas.get(8),
            "cgpa": cgpa,
            "failed_subjects": (
                ",".join(failed_subjects)
                if failed_subjects
                else None
            ),
            "failed_count": len(failed_subjects)
        })

    return students


# =========================================================
# BULK DATABASE UPSERT
#
# SAME ROLL = OVERWRITE
# =========================================================




def save_student_data(students):
    if not students:
        return 0

    # 1. Remove duplicate rolls.
    # Latest occurrence wins.
    student_map = {
        str(student["roll"]): student
        for student in students
    }

    rows = list(student_map.values())
    rolls = list(student_map.keys())

    try:
        # 2. Fetch existing students using SQLAlchemy ORM.
        existing_students = (
            StudentCGPA.query
            .filter(StudentCGPA.roll.in_(rolls))
            .all()
        )

        existing_map = {
            student.roll: student
            for student in existing_students
        }

        # 3. Create or update records.
        for row in rows:
            roll = str(row["roll"])
            student = existing_map.get(roll)

            if student is None:
                student = StudentCGPA(roll=roll)
                db.session.add(student)

            # Update GPA fields.
            student.gpa1 = row.get("gpa1")
            student.gpa2 = row.get("gpa2")
            student.gpa3 = row.get("gpa3")
            student.gpa4 = row.get("gpa4")
            student.gpa5 = row.get("gpa5")
            student.gpa6 = row.get("gpa6")
            student.gpa7 = row.get("gpa7")
            student.gpa8 = row.get("gpa8")

            # Update CGPA and failed subjects.
            student.cgpa = row.get("cgpa")
            student.failed_subjects = row.get(
                "failed_subjects"
            )
            student.failed_count = row.get(
                "failed_count", 0
            )

        # 4. Save all changes in one transaction.
        db.session.commit()

        return len(rows)

    except Exception:
        db.session.rollback()
        raise



# =========================================================
# UPLOAD ROUTE
# =========================================================

@import_pdf_bp.route(
    "/upload-cgpa",
    methods=["GET", "POST"]
)
def upload_cgpa():

    if request.method == "POST":

        uploaded_files = request.files.getlist(
            "pdf_files"
        )

        # -------------------------------------------------
        # VALID PDF FILES
        # -------------------------------------------------

        valid_files = [
            file
            for file in uploaded_files
            if (
                file
                and file.filename
                and allowed_file(file.filename)
            )
        ]

        if not valid_files:

            flash(
                "Please select PDF files.",
                "danger"
            )

            return redirect(
                url_for(
                    "import_pdf.upload_cgpa"
                )
            )

        # -------------------------------------------------
        # UPLOAD DIRECTORY
        # -------------------------------------------------

        upload_folder = os.path.join(
            current_app.instance_path,
            "cgpa_pdfs"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        all_students = []
        import_records = []

        # -------------------------------------------------
        # PROCESS PDFs
        # -------------------------------------------------

        for file in valid_files:

            filename = secure_filename(
                file.filename
            )

            pdf_path = os.path.join(
                upload_folder,
                filename
            )

            try:

                # -----------------------------------------
                # SAVE PDF
                # -----------------------------------------

                file.save(pdf_path)

                # -----------------------------------------
                # PDF -> TEXT
                # -----------------------------------------

                pdf_text = extract_pdf_text(
                    pdf_path
                )

                # -----------------------------------------
                # TEXT -> DATA
                # -----------------------------------------

                students = parse_gpa_data(
                    pdf_text
                )

                all_students.extend(
                    students
                )

                # -----------------------------------------
                # IMPORT HISTORY
                # -----------------------------------------

                import_records.append(
                    CGPAImportFile(
                        filename=filename
                    )
                )

            except Exception:

                current_app.logger.exception(
                    f"CGPA PDF processing failed: {filename}"
                )

                flash(
                    f"{filename}: PDF processing failed.",
                    "danger"
                )

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        try:

            # Save import history
            if import_records:

                db.session.add_all(
                    import_records
                )

            # Bulk UPSERT students
            total_students = save_student_data(
                all_students
            )

            # ONE COMMIT
            db.session.commit()

            flash(
                f"{len(import_records)} PDF uploaded successfully. "
                f"{total_students} student records saved/updated.",
                "success"
            )

        except Exception as e:

            db.session.rollback()

            current_app.logger.exception(
                "CGPA database save failed"
            )

            flash(
                f"Database error: {str(e)}",
                "danger"
            )

        return redirect(
            url_for(
                "import_pdf.upload_cgpa"
            )
        )

    # =====================================================
    # GET
    # =====================================================

    files = (
        CGPAImportFile.query
        .order_by(
            CGPAImportFile.id.desc()
        )
        .all()
    )

    return render_template(
        "admin/upload/upload_cgpa.html",
        files=files
    )

