# !/usr/bin/env python
# coding: utf-8
from flask_helper.utils.log import DummyLog


__author__ = 'zhouhenglc'


class FlaskHook(object):
    priority = 100  # register the low priority first

    def __init__(self, app):
        self.app = app
        self.log = DummyLog()
        if hasattr(self.app, 'log'):
            self.log = self.app.log

    def before_request(self):
        pass

    def after_request(self, response):
        return response
