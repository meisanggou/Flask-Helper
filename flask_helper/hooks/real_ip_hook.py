# !/usr/bin/env python
# coding: utf-8
from flask import request, g, make_response

from flask_helper.flask_hook import FlaskHook
from flask_helper.utils.ip import ip_value_str
from flask_helper.globals import extra_request_ctx

__author__ = 'zhouhenglc'


class RealIPHook(FlaskHook):

    def __init__(self, app, trust_proxy=None,
                 forwarded_key="X-Forwarded-For"):
        FlaskHook.__init__(self, app)
        if trust_proxy is None:
            trust_proxy = []
        self.trust_proxy = list(trust_proxy)
        self.forwarded_key = forwarded_key

    def before_request(self):
        request_ip = request.remote_addr
        if self.forwarded_key in request.headers \
                and request_ip in self.trust_proxy:
            l_ip = request.headers[self.forwarded_key].split(",")
            request_ip = l_ip[0]
            if isinstance(self.trust_proxy, list):
                for i in range(len(l_ip) - 1, -1, -1):
                    one_proxy = l_ip[i].strip()
                    if one_proxy not in self.trust_proxy:
                        request_ip = one_proxy
                        break
        g.remote_addr = request_ip
        extra_request_ctx.set_value('request_ip', request_ip)
        g.ip_value = ip_value_str(ip_str=request_ip)
        if g.ip_value == 0:
            return make_response("IP受限", 403)
