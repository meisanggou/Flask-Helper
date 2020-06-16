# !/usr/bin/env python
# coding: utf-8
from flask import request

from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class Handle30xHook(FlaskHook):
    priority = 110

    def __init__(self, app, protocol_key="X-Request-Protocol"):
        FlaskHook.__init__(self, app)
        self.protocol_key = protocol_key

    def after_request(self, response):
        if response.status_code > 302 or response.status_code < 301:
            return response
        if self.protocol_key in request.headers:
            pro = request.headers[self.protocol_key]
            if "Location" in response.headers:
                location = response.headers["location"]
                if location.startswith("http:"):
                    response.headers["Location"] = pro + ":" + response.headers["Location"][5:]
                elif location.startswith("/"):
                    response.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
        return response
