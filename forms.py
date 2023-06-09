from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3

class LoginForm(FlaskForm):
        username = StringField('Login', validators=[DataRequired()])
        password = PasswordField('Hasło', validators=[DataRequired()])
        remember = BooleanField('Zapamiętaj mnie')
        submit = SubmitField('Login')