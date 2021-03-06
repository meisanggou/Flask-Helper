# !/usr/bin/env python
# coding: utf-8
import re

from flask import request, make_response

from flask_helper.flask_hook import FlaskHook

__author__ = 'zhouhenglc'


class UserAgentHook(FlaskHook):
    priority = 110

    def __init__(self, app, *accept_agent, ignore_paths=None):
        FlaskHook.__init__(self, app)
        self.accept_agent = []
        for item in accept_agent:
            self.accept_agent.extend(item.split("|"))
        self.re_agent = "(%s)" % "|".join(map(lambda x: re.escape(x),
                                              self.accept_agent))
        self.pattern = re.compile(self.re_agent, re.I)
        if ignore_paths:
            re_ignore_paths = "(%s)" % "|".join(ignore_paths)
            self._i_pattern = re.compile(re_ignore_paths, re.I)
        else:
            self._i_pattern = None

    def before_request(self):
        if self._i_pattern and self._i_pattern.match(request.path):
            self.app.log.debug('User Agent Hook ignore path %s', request.path)
            return
        if "User-Agent" not in request.headers:
            self.app.log.warn('Request headers not content User-Agent, '
                              'path is %s', request.path)
            return make_response("Forbidden", 403)
        user_agent = request.headers["User-Agent"]
        s_agent = self.pattern.search(user_agent)
        if s_agent is None:
            self.app.log.warn('Request User-Agent %s not allow, '
                              'path is %s', user_agent, request.path)
            return make_response("Forbidden", 403)
