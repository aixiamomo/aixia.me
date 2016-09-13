# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    TextAreaField, BooleanField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, URL
from flask_pagedown.fields import PageDownField


class LoginForm(Form):  # 用户登录表单
    email = StringField('Email address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class PostForm(Form):
    body = PageDownField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SettingForm(Form):
    """博客常规设置"""
    blog_title = StringField(u'标题', validators=[DataRequired()])
    blog_description = StringField(u'二级标题', validators=[DataRequired()])
    blog_cover = StringField(u'封面图Url', validators=[DataRequired(), URL()])
    Posts_per_page = IntegerField(u'每页显示的文章数', validators=[DataRequired()])
    author_detail = TextAreaField(u'个人简介', validators=[DataRequired()])
    submit = SubmitField(u'保存')


class EditorForm(Form):
    """文章编辑"""
    title = StringField(u'标题', validators=[DataRequired()])
    cover = StringField(u'封面图')
    url_name = StringField(u'Post URL', validators=[DataRequired()])
    editor = TextAreaField(u'正文', validators=[DataRequired()])
    summary = TextAreaField(u'文章摘要')
    publish = BooleanField(u'发布')
    publish_date = DateField(u'发表日期')
    tags = StringField(u'标签')
    submit = SubmitField(u'保存')


class TagForm(Form):
    cover = StringField(u'封面图')
    name = StringField(u'标签名')
    url_name = StringField(u'Tag URL')
    submit = SubmitField(u'保存')

