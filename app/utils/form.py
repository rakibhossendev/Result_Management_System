from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo


class SearchForm(FlaskForm):
    roll = StringField("Enter Roll Number",
        validators=[
            DataRequired(),
            Length(min=1, max=10)
        ]
    )

    submit = SubmitField("Search")


class LoginForm(FlaskForm):
    username = StringField("Enter username",
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    password = PasswordField("Password",
        validators=[
            DataRequired(),
            Length(min=1, max=32)
        ]
    )
    submit = SubmitField("Login")


class PrincipalDataForm(FlaskForm):

    principal_id = StringField("Enter id",
        validators=[
            DataRequired(),
            Length(min=3, max=10)
        ]
    )

    first_name = StringField("Enter First name",
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    last_name = StringField("Enter last name",
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    mobile_number = StringField("Enter Phone number",
        validators=[
            DataRequired(),
            Length(min=11, max=11),
            Regexp(
                r'^\d{11}$',
                message="Enter a valid 11-digit phone number"
            )
        ]
    )

    email = StringField("Enter email",
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    institute = StringField("Enter Institute Name",
        validators=[
            DataRequired(),
            Length(min=1, max=200)
        ]
    )

    institute_code = StringField("Enter institute Code",
        validators=[
            DataRequired(),
            Length(min=1, max=20)
        ]
    )
    
    username = StringField("Enter username",
        validators=[
            DataRequired(),
            Length(min=6,max=120)
        ]
    )
    
    password = PasswordField("Enter a Strong Password",
        validators=[
            DataRequired(),
            Length(min=6, max=32)
        ]
    )

    retype_password = PasswordField("Retype password",
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField("Add Principal")


class ShiftSelectForm(FlaskForm):
    
    shift = SelectField("Select Shift",
        choices=[
            ("Morning", "Morning Shift"),
            ("Day", "Day Shift")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Continue")