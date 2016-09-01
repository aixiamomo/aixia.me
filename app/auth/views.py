# -*- coding: utf-8 -*-
from . import auth
from flask import render_template


@auth.route('/login')
def login():
    render_template('index.html')
