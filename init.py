# -*- coding: utf-8 -*-
from app import db, create_app
from app.models import User, Post

app = create_app()

with app.app_context():
    db.create_all()
    u = User()
    u.email = 'admin@admin.com'
    u.password = 'password'
    db.session.add(u)
    db.session.commit()
    # Post.generate_fake()
