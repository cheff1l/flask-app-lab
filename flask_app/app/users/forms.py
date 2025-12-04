from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app.users.models import User
from app import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=16),
        Regexp('^[A-Za-z][A-Za-z0-9_.-]*$', message="Username must start with a letter and contain only letters, numbers, dots or underscores.")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    
    submit = SubmitField('Register Now')
    
    def validate_email(self, email):
        user = db.session.execute(db.select(User).where(User.email == email.data)).scalar_one_or_none()
        if user:
            raise ValidationError('Email is already registered.')
    
    def validate_username(self, username):
        user = db.session.execute(db.select(User).where(User.username == username.data)).scalar_one_or_none()
        if user:
            raise ValidationError('Username must have only letters, numbers, dots or underscores.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')
