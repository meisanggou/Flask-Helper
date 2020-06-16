# !/usr/bin/env python
# coding: utf-8


__author__ = 'zhouhenglc'


class FlaskHook(object):
    priority = 100

    def __init__(self, app):
        self.app = app

    def before_request(self):
        pass

    def after_request(self, response):
        return response
