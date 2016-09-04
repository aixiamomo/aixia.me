# -*- coding: utf-8 -*-
from app import db, create_app
from app.models import User, Post

app = create_app()

with app.app_context():
    db.create_all()
    u = User()
    u.email = '920534583@qq.com'
    u.password = 'qq920534583'
    db.session.add(u)
    db.session.commit()
    Post.generate_fake()

