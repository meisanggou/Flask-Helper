# !/usr/bin/env python
# coding: utf-8
import uuid

from flask import g
from flask_helper.flask_hook import FlaskHook
from flask_helper.globals import extra_request_ctx


__author__ = 'zhouhenglc'


class RequestIDHook(FlaskHook):
    priority = 50

    def __init__(self, app, response_header=None, submit_func=None):
        super().__init__(app)
        if not response_header:
            response_header = 'X-Request-ID'
        self.response_header = response_header
        self.submit_func = submit_func

    def before_request(self):
        _uuid = str(uuid.uuid4())
        request_id = 'req-%s' % _uuid
        g.request_id = request_id
        extra_request_ctx.set_value('request_id', request_id)
        if self.submit_func:
            self.submit_func(request_id)

    def after_request(self, response):
        response.headers[self.response_header] = g.request_id
        return response
