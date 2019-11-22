# Here we create our forms

__author__ = 'Christian Ramírez de León'

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, Regexp, Length, EqualTo
from models import User
from wtforms import TextAreaField


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError(' The username already exists')


def email_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError(' The user with that email already exists')


class RegisterForm(FlaskForm):
    """ The username variable is automatically passed as an argument to the method in the name_exists validators """
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$'
            ),
            name_exists
        ]
    )
    """ The email variable is automatically passed as an argument to the method in the name_exists validators """
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    """ The password variable is automatically passed as an argument to the method in the name_exists validators """
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(FlaskForm):
    content = TextAreaField('What You Think?', validators=[DataRequired(), Length(max=255)])