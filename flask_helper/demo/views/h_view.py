# !/usr/bin/env python
# coding: utf-8
from flask_helper.view import View

__author__ = 'zhouhenglc'

h_view = View('h_view', __name__, url_prefix='/h')
h2_view = h_view


@h_view.route('/abc')
@h_view.route('/abc/ping')
def index():
    return 'h success'
