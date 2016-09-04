# -*- coding: utf-8 -*-
import datetime
from . import db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
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


belong_to = db.Table('belong_to',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    cover = db.Column(db.String(64))
    content = db.Column(db.Text)
    markdown = db.Column(db.Text)
    publish = db.Column(db.Boolean, default=True, index=True)

    create_date = db.Column(db.DateTime, default=datetime.date.today())
    update_date = db.Column(db.DateTime, default=datetime.date.today())

    tags = db.relationship('Tag',
                           secondary=belong_to,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    @staticmethod
    def generate_fake(count=20):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Post(title=forgery_py.internet.user_name(True),
                     content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     create_date=forgery_py.date.date(True),
                     )
            db.session.add(p)
            db.session.commit()


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url_name = db.Column(db.String(64), index=True)

    create_date = db.Column(db.DateTime, default=datetime.date.today())
    update_date = db.Column(db.DateTime, default=datetime.date.today())


@login_manager.user_loader
def load_user(id_user):
    """加载用户的回调函数"""
    return User.query.get(int(id_user))
