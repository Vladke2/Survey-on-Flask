from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    age = StringField("Age: ", validators=[DataRequired(), Length(max=4)])
    submit = SubmitField("Register")
