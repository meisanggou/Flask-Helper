# !/usr/bin/env python
# coding: utf-8
import re

from flask import request, make_response

from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class UserAgentHook(FlaskHook):
    priority = 110

    def __init__(self, app, *accept_agent):
        FlaskHook.__init__(self, app)
        self.accept_agent = []
        for item in accept_agent:
            self.accept_agent.extend(item.split("|"))
        self.re_agent = "(%s)" % "|".join(map(lambda x: re.escape(x),
                                              self.accept_agent))
        self.pattern = re.compile(self.re_agent, re.I)

    def before_request(self):
        if "User-Agent" not in request.headers:
            return make_response("Forbidden", 403)
        user_agent = request.headers["User-Agent"]
        s_agent = self.pattern.search(user_agent)
        if s_agent is None:
            return make_response("Forbidden", 403)
