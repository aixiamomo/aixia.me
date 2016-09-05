# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 记录登陆IP和代理信息，异常就登出用户
login_manager.login_view = 'admin.login'  # 登陆页面的端点
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    from .admin import admin as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/admin')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
