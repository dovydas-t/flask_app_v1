from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    submit =SubmitField('Register')

class ProfileDetailsForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=3, max=20)])
    name = StringField('Name', validators=[Length(min=2, max=30)])
    email = StringField('Email', validators=[Length(min=6, max=35)])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[])
    submit = SubmitField('Update Details')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')
