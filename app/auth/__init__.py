# -*- coding: utf-8 -*-
from flask import Blueprint

auth = Blueprint('auth', __name__)  # 实例化蓝本

from . import views  # 从当前包下导入views模型，与蓝本关联起来
