# -*- coding: utf-8 -*-
from flask import Blueprint

admin = Blueprint('admin', __name__, static_folder='static')  # 实例化蓝本

from . import views  # 从当前包下导入views模型，与蓝本关联起来
