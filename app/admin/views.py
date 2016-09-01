# -*- coding: utf-8 -*-
from . import admin
from .forms import LoginForm
from flask import render_template


@admin.route('/login')
def login():
    form = LoginForm
    return render_template('admin/login.html', form=form)
