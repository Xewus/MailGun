# This Python file uses the following encoding: utf-8
 
from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, PasswordField, RadioField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired, Length, NumberRange

from src.settings import (MAX_CELERY_DELAY, MAX_LENGTH_EMAIL,
                               MAX_LENGTH_PASSWORD, MAX_LENGTH_USERNAME)
from src.core.validators import EmailValidator


class LoginForm(FlaskForm):
    username = StringField(
        label=u'От чьёго имени производить рассылку',
        validators=[
            DataRequired(message='Напишите имя или название'),
            Length(max=MAX_LENGTH_USERNAME)
        ]
    )
    user_email = StringField(
        label=u'Google-email, с которого будет производиться рассылка.',
        validators=[
            DataRequired(message=u'Напишите email'),
            Length(max=MAX_LENGTH_EMAIL, min=6),
            EmailValidator()
        ]
    )
    password = PasswordField(
        label=u'Пароль приложения для доступа к почте',
        validators=[
            DataRequired(message=u'Напишите пароль доступа'),
            Length(max=MAX_LENGTH_PASSWORD)
        ]
    )
    remember_me = BooleanField(
        label=u'Запомнить меня'
    )
    submit = SubmitField(
        label=u'Начать пользоваться'
    )


class AddContactForm(FlaskForm):
    contact_email = StringField(
        label=u'Электронная почта адресата',
        validators=[
            DataRequired(message=u'Напишите электронную почту'),
            Length(max=MAX_LENGTH_EMAIL, min=6),
            EmailValidator()
        ]
    )
    contact_name = StringField(
        label=u'Имя адресата',
        validators=[
            DataRequired(message=u'Напишите имя адресата'),
            Length(max=MAX_LENGTH_USERNAME)
        ]
    )
    submit = SubmitField(
        label=u'Добавить'
    )


class ChoiceTemplateForm(FlaskForm):
    choice = RadioField(
        label=u'Выбрать шаблон для отправки',
        validators=[DataRequired()],
        choices=[]
    )
    countdown = IntegerField(
        label=u'Отложить отправку на указанное количество часов',
        validators=[
            NumberRange(min=0, max=MAX_CELERY_DELAY)
        ],
        default = 0
    )
    submit = SubmitField(
        label=u'Начать рассылку'
    )
