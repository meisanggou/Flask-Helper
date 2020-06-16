#! /usr/bin/env python
# coding: utf-8

import re
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.serving import run_simple
from flask_helper._flask import FlaskHelper

__author__ = '鹛桑够'


app = FlaskHelper(__name__)
app.cross_domain()
app.cross_domain()
app.filter_user_agent()
app.handle_30x()
app.real_ip()
# app.real_ip()


@app.route("/")
def index():
    # from flask_helper import remote_addr
    # print(remote_addr)
    return "success"


class MyMiddleware(object):

    def __init__(self, wsgi_app, accept_agent=None):
        if accept_agent is None:
            accept_agent = "(firefox|chrome|safari|window|GitHub|jyrequests|micro|Aliyun)"
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        if "HTTP_USER_AGENT" not in environ:
            status_code = 403
            status = "%s %s" % (status_code, HTTP_STATUS_CODES.get(status_code, ""))
            headers = [("Content-Type", "text/html")]
            start_response(status, headers)
            return ""
        user_agent = environ["HTTP_USER_AGENT"]
        path_info = environ["PATH_INFO"]
        print("middleware")
        print(environ)
        for k, v in environ.items():
            print("%s : %s" % (k, v))
            # print(v)
        if path_info == "/404":
            status = "404 %s" % HTTP_STATUS_CODES.get(404, "")
            headers = [("Content-Type", "text/html")]
            start_response(status, headers)
            return ""
        result = self.wsgi_app(environ, start_response)

        return result


# app.wsgi_app = MyMiddleware(app.wsgi_app)


if __name__ == "__main__":
    run_simple("127.0.0.1", 8080, app)
    # app.run(port=10000)