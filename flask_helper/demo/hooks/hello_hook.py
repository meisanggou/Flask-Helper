# !/usr/bin/env python
# coding: utf-8
from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class HelloHook(FlaskHook):

    def __init__(self, app):
        FlaskHook.__init__(self, app)

    def before_request(self):
        print('enter hello hook')

    def after_request(self, response):
        return response
