'''There is AddStudentForm and SelectSemesterAndDepartmentForm'''

from flask_wtf import FlaskForm
from wtforms import SelectField,IntegerField,StringField,SubmitField,DateTimeField
from wtforms.validators import DataRequired
from wtforms import SelectField

class AddStudentForm(FlaskForm):

    student_roll = IntegerField("Student Roll",validators=[DataRequired()])
    student_full_name = StringField("Student Name",validators=[DataRequired()])
    department_id = SelectField("Department",coerce=int, choices=[])
    semester = SelectField("Semester",coerce=int,choices=[
            (1,"Semester 1"),
            (2,"Semester 2"),
            (3,"Semester 3"),
            (4,"Semester 4"),
            (5,"Semester 5"),
            (6,"Semester 6"),
            (7,"Semester 7"),
            (8,"Semester 8"),
        ]
    )
    group = SelectField("If exit. Select group",choices=[("None"),("A"),("B")])
    submit = SubmitField("Add Student")



class SelectSemesterAndDepartmentForm(FlaskForm):
    
    department_id = SelectField("Select Department",choices=[],coerce=int)
    semester = SelectField("Select Semester",choices=[],coerce=int)
    group = SelectField("Select Group",choices=[])
    submit = SubmitField("Load Student")