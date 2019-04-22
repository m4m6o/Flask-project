# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
 
 
class RegForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    license = BooleanField('Принимаю лицензионное соглашение: "http://pasted.co/dbd45cee"', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')