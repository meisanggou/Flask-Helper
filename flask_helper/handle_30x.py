#! /usr/bin/env python
# coding: utf-8

from flask import request

__author__ = '鹛桑够'


class Handle30X(object):

    def __init__(self, app, protocol_key="X-Request-Protocol"):
        self.protocol_key = protocol_key
        app.after_request_funcs.setdefault(None, []).append(self.support_30x)

    def support_30x(self, res):
        if res.status_code > 302 or res.status_code < 301:
            return res
        if self.protocol_key in request.headers:
            pro = request.headers[self.protocol_key]
            if "Location" in res.headers:
                location = res.headers["location"]
                if location.startswith("http:"):
                    res.headers["Location"] = pro + ":" + res.headers["Location"][5:]
                elif location.startswith("/"):
                    res.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
        return res
