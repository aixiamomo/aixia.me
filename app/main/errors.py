# -*- coding: utf-8 -*-
from flask import render_template
from . import main
from app.models import User


@main.app_errorhandler(404)
def page_not_found(e):
    user = User.query.get_or_404(1)
    return render_template('404.html', user=user), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    user = User.query.get_or_404(1)
    return render_template('500.html', user=user), 500
