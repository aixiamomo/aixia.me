# -*- coding:utf-8 -*-
import os
# from flask import session

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'you-will-never-guess'
CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
MANAGE_POSTS_PER_PAGE = 8  # 管理文章中分页的显示的文章数量
MAX_SEARCH_RESULTS = 50  # 搜索结果返回的最大数量

WHOOSH_BASE = os.path.join(basedir, 'search.db')

# session.permanent = True
