from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    '''There is Attendance form code. '''
    
    attendance_date = DateField("Select Date",validators=[DataRequired()])
    department_id = SelectField("Department",coerce=int,choices=[])
    semester = SelectField("Semester",coerce=int,choices=[])
    group = SelectField("Group",choices=[])
    submit = SubmitField("Load Students")