from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from validators import validate_vin, validate_unique_username, validate_unique_email

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20), validate_unique_username])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=30)])
    email =StringField('Email',validators=[DataRequired(), Length(min=6, max=35), validate_unique_email])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    vin = StringField('VIN', validators=[DataRequired(), Length(min=17, max=17), validate_vin])
    submit =SubmitField('Register')

    def __init__(self, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = model


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


