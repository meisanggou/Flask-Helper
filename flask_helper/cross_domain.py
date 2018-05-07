#! /usr/bin/env python
# coding: utf-8
__author__ = 'meisanggou'


class FlaskCrossDomain(object):
    """
        add in 0.1
    """

    def __init__(self, app):
        allow_methods = app.config.get("ACCESS_CONTROL_ALLOW_METHODS", ["POST", "GET", "PUT", "DELETE"])
        if isinstance(allow_methods, list) or isinstance(allow_methods, tuple):
            self.allow_methods = ",".join(allow_methods)
        elif isinstance(allow_methods, unicode):
            self.allow_methods = allow_methods
        else:
            self.allow_methods = str(allow_methods)
        allow_origin = app.config.get("ACCESS_CONTROL_ALLOW_ORIGIN", "*")
        if isinstance(allow_origin, unicode):
            self.allow_origin = allow_origin
        else:
            self.allow_origin = str(allow_origin)
        allow_headers = app.config.get("ACCESS_CONTROL_ALLOW_HEADERS", "Content-Type,Authorization")
        if isinstance(allow_headers, list) or isinstance(allow_headers, tuple):
            self.allow_headers = ",".join(allow_headers)
        elif isinstance(allow_headers, unicode):
            self.allow_headers = allow_headers
        else:
            self.allow_headers = str(allow_headers)
        self._disabled_cross_domain = app.config.get("DISABLED_CROSS_DOMAIN", False)
        app.after_request_funcs.setdefault(None, []).append(self.add_cross_domain_headers)

    def add_cross_domain_headers(self, resp):
        if self._disabled_cross_domain is True:
            return resp
        resp.headers["Access-Control-Allow-Methods"] = self.allow_methods
        resp.headers["Access-Control-Allow-Origin"] = self.allow_origin
        resp.headers["Access-Control-Allow-Headers"] = self.allow_headers
        return resp
