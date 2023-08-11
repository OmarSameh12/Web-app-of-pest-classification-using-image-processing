from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from runn.models import User


class RegistrationForm(FlaskForm):

    name = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)] )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Regexp(
                                                         "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$")])
    # confirm_password = PasswordField(
    #     "Confirm_Password", validators=[DataRequired(), EqualTo("password")]
    # )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please chosse a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please chosse a different one")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class predictForm(FlaskForm):
    image=FileField("upload image",validators=[FileAllowed(['png','jpg'])])