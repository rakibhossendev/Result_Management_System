from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddMarksForm(FlaskForm):
    ''' There is AddMarks Form code'''
    
    subject = SelectField("Subject",coerce=int,choices=[],validators=[DataRequired()])
    marks_topic = SelectField("Marks Topic",coerce=int,choices=[],validators=[DataRequired()])
    get_marks = IntegerField("Obtained Marks",validators=[DataRequired()])
    submit = SubmitField("Save Marks")