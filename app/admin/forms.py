# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_pagedown.fields import PageDownField


class LoginForm(Form):  # 用户登录表单
    email = StringField('Email address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(Form):
    body = PageDownField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
