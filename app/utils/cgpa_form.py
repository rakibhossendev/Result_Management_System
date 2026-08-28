from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class UploadCGPAForm(FlaskForm):
    pdf = FileField("Upload PDF",validators=[FileRequired()])
    submit = SubmitField("Upload")