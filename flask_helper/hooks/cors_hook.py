# !/usr/bin/env python
# coding: utf-8
from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class CorsHook(FlaskHook):
    priority = 110
    default_methods = ['POST', 'PUT', 'DELETE', 'GET']
    default_origin = '*'
    default_headers = ['Content-Type']

    def __init__(self, app, **kwargs):
        FlaskHook.__init__(self, app)
        methods = kwargs.pop('methods', self.default_methods)
        self.allow_methods = ','.join(methods)
        self.allow_origin = kwargs.pop('origin', self.default_origin)
        headers = kwargs.pop('headers', self.default_headers)
        self.allow_headers = ','.join(headers)

    def after_request(self, response):
        response.headers['Access-Control-Allow-Methods'] = self.allow_methods
        response.headers['Access-Control-Allow-Origin'] = self.allow_origin
        response.headers['Access-Control-Allow-Headers'] = self.allow_headers
        return response
