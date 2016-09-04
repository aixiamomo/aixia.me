# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'you-will-never-guess'
CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASKY_POSTS_PER_PAGE = 8

