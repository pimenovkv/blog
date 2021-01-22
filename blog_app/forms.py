from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from blog_app.models import Users


class LoginForm(FlaskForm):
    """
    Класс, описывающий форму входа пользователя
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrForm(FlaskForm):
    """
    Класс, описывающий форму регистрации пользователя
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_<field_name>(self, field_name)
    # Функции такого формата являются пользовательскими валидаторами
    def validate_username(self, username):
        user = Users.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class NewPostForm(FlaskForm):
    """
    Класс, описывающий форму написания нового поста
    """
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post', validators=[DataRequired()])
    submit = SubmitField('Submit')
