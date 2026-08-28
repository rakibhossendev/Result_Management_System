from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired

class MarksTopicForm(FlaskForm):
    department_id = SelectField("Department",choices=[],validators=[DataRequired()])
    subject = SelectField("Subject",choices=[],validators=[DataRequired()])
    add_marks_topic_name = StringField("Marks Topic Name",validators=[DataRequired()])
    full_marks = IntegerField("Full Marks",validators=[DataRequired()])
    
    submit = SubmitField("Add Marks System")