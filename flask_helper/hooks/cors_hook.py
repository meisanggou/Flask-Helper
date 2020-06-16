# !/usr/bin/env python
# coding: utf-8
from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class CorsHook(FlaskHook):
    priority = 110

    def __init__(self, app):
        FlaskHook.__init__(self, app)
        self.allow_methods = ','.join(['POST', 'PUT', 'DELETE', 'GET'])
        self.allow_origin = '*'
        self.allow_headers = 'Content-Type'

    def after_request(self, response):
        response.headers['Access-Control-Allow-Methods'] = self.allow_methods
        response.headers['Access-Control-Allow-Origin'] = self.allow_origin
        response.headers['Access-Control-Allow-Headers'] = self.allow_headers
        return response
