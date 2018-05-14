#! /usr/bin/env python
# coding: utf-8

from flask import request, make_response, g
from flask_helper.util.ip import ip_value_str

__author__ = '鹛桑够'


class RealIP(object):

    def __init__(self, app, trust_proxy=None):
        if trust_proxy is None:
            trust_proxy = []
        self.trust_proxy = list(trust_proxy)
        app.before_request_funcs.setdefault(None, []).append(self.receive_real_ip)

    def receive_real_ip(self):
        request_ip = request.remote_addr
        if "X-Forwarded-For" in request.headers and request_ip in self.trust_proxy:
            l_ip = request.headers["X-Forwarded-For"].split(",")
            request_ip = l_ip[0]
            if isinstance(self.trust_proxy, list):
                for i in range(len(l_ip) - 1, -1, -1):
                    one_proxy = l_ip[i].strip()
                    if one_proxy not in self.trust_proxy:
                        request_ip = one_proxy
                        break
        g.remote_addr = request_ip
        g.ip_value = ip_value_str(ip_str=request_ip)
        if g.ip_value == 0:
            return make_response("IP受限", 403)
