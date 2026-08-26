from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired

class ChangePasswordForm(FlaskForm):
    username = StringField("Enter New Username",validators=[DataRequired()])
    new_password = PasswordField("Enter new password", validators=[DataRequired()])
    old_password = PasswordField("Enter old Password",validators=[DataRequired()])
    submit = SubmitField("Save")