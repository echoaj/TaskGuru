from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

from flaskr.models import User


class SignUpForm(FlaskForm):
    # 1 Not blank user name
    # 2 Short user name
    rules = [InputRequired(), Length(min=3, max=8)]
    username = StringField('Username', validators=rules)
    # 3 Valid email
    rules = [InputRequired(), Email()]
    email = StringField('Email', validators=rules)
    # 4 Valid Password
    rules = [InputRequired(), Length(min=4), EqualTo('confirm', message='Passwords must match')]
    password = PasswordField('Password', validators=rules)
    confirm = PasswordField('Confirm Password')
    # 5 Submit
    submit = SubmitField('Sign Up')

    # check to see if user already exists in database
    # query database for username and check if exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.  Choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken.  Choose a different one.')


class LoginForm(FlaskForm):
    # 3 Valid email
    rules = [InputRequired(), Email()]
    email = StringField('Email', validators=rules)
    # 4 Valid Password
    rules = [InputRequired(), Length(min=4)]
    password = PasswordField('Password', validators=rules)
    remember = BooleanField('Remember Me')
    # 5 Submit
    submit = SubmitField('Log In')
