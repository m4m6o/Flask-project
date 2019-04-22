# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired
 
 
class CommentForm(FlaskForm):
    content = TextAreaField('Оставьте Ваш комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')