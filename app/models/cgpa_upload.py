from app.extensions import db


class CGPAImportFile(db.Model):
    __tablename__ = "cgpa_import_files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime,server_default=db.func.now())


class StudentCGPA(db.Model):
    __tablename__ = "student_cgpa"

    id = db.Column(db.Integer, primary_key=True)

    roll = db.Column(db.String(20),unique=True,nullable=False,index=True)
    # Semester GPA
    gpa1 = db.Column(db.Float, nullable=True)
    gpa2 = db.Column(db.Float, nullable=True)
    gpa3 = db.Column(db.Float, nullable=True)
    gpa4 = db.Column(db.Float, nullable=True)
    gpa5 = db.Column(db.Float, nullable=True)
    gpa6 = db.Column(db.Float, nullable=True)
    gpa7 = db.Column(db.Float, nullable=True)
    gpa8 = db.Column(db.Float, nullable=True)
    cgpa = db.Column(db.Float, nullable=True)

    # Example:
    # 25931:T,26811:T,26932:T
    failed_subjects = db.Column(db.Text,nullable=True)
    failed_count = db.Column(db.Integer,default=0)