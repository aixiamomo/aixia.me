# -*- coding:utf-8 -*-
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Post, Tag, belong_to
# import flask_whooshalchemy as whooshalchemy


app = create_app()
manage = Manager(app)
migrate = Migrate(app, db)

# whooshalchemy.whoosh_index(app, Post)  # 给Post建立全文搜索


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, belong_to=belong_to)

manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)
manage.add_command('runserver', Server('127.0.0.1', port=5000))

if __name__ == '__main__':
    manage.run()
