# -*- coding: utf-8 -*-
import datetime
from . import db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'admin'
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # 与存储在User模型中的密码散列值对比
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'post'
    id_post = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    markdown = db.Column(db.Text)

    create_date = db.Column(db.DateTime, default=datetime.date.today())
    update_date = db.Column(db.DateTime, default=datetime.date.today())

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id_tag'))


class Tag(db.Model):
    __tablename__ = 'tag'
    id_tag = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    create_date = db.Column(db.DateTime, default=datetime.date.today())
    update_date = db.Column(db.DateTime, default=datetime.date.today())

    post_set = db.relationship('Post', backref='tag', lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    """加载用户的回调函数"""
    return User.query.get(int(user_id))
