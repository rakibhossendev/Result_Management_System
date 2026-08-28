from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired

class CurriculamForm(FlaskForm):
    
    department_id = SelectField("Department",choices=[],coerce=int,validators=[DataRequired()])
    semester = SelectField("Semester",choices=[(i, f"Semester {i}") for i in range(1, 9)],coerce=int,validators=[DataRequired()])
    subject_id = SelectField("Subject",choices=[],coerce=int,validators=[DataRequired()])

    submit = SubmitField("Assign Subject")


class DepartmentForm(FlaskForm):
    
    department_code = IntegerField("Department Code",validators=[DataRequired()])
    department_name = StringField("Department Name",validators=[DataRequired()])

    submit = SubmitField("Save Department")


class SubjectForm(FlaskForm):
    subject_code = StringField("Subject Code",validators=[DataRequired()])
    subject_name = StringField("Subject Name",validators=[DataRequired()])
    submit = SubmitField("Save Subject")


class TeacherAssignmentForm(FlaskForm):
    
    teacher_id = SelectField(choices=[],coerce=int,validators=[DataRequired()])
    department_id = SelectField(choices=[],coerce=int,validators=[DataRequired()])
    semester = SelectField(choices=[(i, f"Semester {i}") for i in range(1, 9)],coerce=int,validators=[DataRequired()])
    subject_id = SelectField(choices=[],coerce=int,validators=[DataRequired()])

    submit = SubmitField("Assign Teacher")