#! /usr/bin/env python
# coding: utf-8

import sys
import re
from datetime import datetime
from flask import Flask, g, jsonify, request, make_response, send_from_directory
from .ctx import RequestContext2
from user_agent import FilterUserAgent
from cross_domain import FlaskCrossDomain
from handle_30x import Handle30X
from ip import RealIP
from sessions import SecureCookieSessionInterface2
from flask_helper.url_rule import UrlRules, UrlRule


__author__ = '鹛桑够'


#  内置_Flask2 增加 app_url_prefix即所有注册路由的前缀 添加APP运行时间 run_time 自动注册handle500
class _Flask2(Flask):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, import_name, **kwargs):
        self.app_url_prefix = kwargs.pop('url_prefix', "").rstrip("/")
        self.run_time = datetime.now().strftime(self.TIME_FORMAT)
        self._broken_rules = set()
        super(_Flask2, self).__init__(import_name, **kwargs)
        self.register_error_handler(500, self._handle_500)

    def add_broken_rule(self, rule):
        if isinstance(rule, (str, unicode)):
            self._broken_rules.add(rule)

    def clear_broken_rules(self):
        self._broken_rules.clear()

    def remove_broken_rule(self, rule):
        self._broken_rules.remove(rule)

    def list_broken_rules(self):
        return list(self._broken_rules)

    def run(self, host=None, port=None, debug=None, **options):
        self.run_time = datetime.now().strftime(_Flask2.TIME_FORMAT)
        if port is not None and port <= 0:
            sys.stderr.write("Not run. port must greater than 0.\n")
            return None
        super(_Flask2, self).run(host=host, port=port, debug=debug, **options)

    def add_url_rule2(self, url_rule):
        assert isinstance(url_rule, UrlRule)
        self.add_url_rule(url_rule.rule, url_rule.endpoint, url_rule.view_func, **url_rule.options)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        rule = self.app_url_prefix + rule
        for item in self._broken_rules:
            if re.search(item, rule) is not None:
                sys.stderr.write("Not add %s, is broken rule\n" % rule)
                return None
        super(_Flask2, self).add_url_rule(rule=rule, endpoint=endpoint, view_func=view_func, **options)

    def send_static_file2(self, filename, static_folder=None):
        if static_folder is None:
            if not self.has_static_folder:
                raise RuntimeError('No static folder for this object')
            static_folder = self.static_folder

        cache_timeout = self.get_send_file_max_age(filename)
        return send_from_directory(static_folder, filename, cache_timeout=cache_timeout)

    def request_context(self, environ):
        return RequestContext2(self, environ)

    def _handle_500(self, e):
        resp = jsonify({"status": self.config.get("ERROR_STATUS", 99), "message": str(e)})
        return resp


class Flask2(_Flask2):

    session_interface = SecureCookieSessionInterface2()

    @staticmethod
    def _assign_default_g():
        pass

    @staticmethod
    def _packet_data():
        # if request.method == "OPTIONS":
        #     return make_response("success", 204)
        if request.method != "GET":
            if request.json is None:
                g.request_data = {}
            else:
                g.request_data = request.json
            if type(g.request_data) != dict:
                return make_response("访问受限", 400)
        else:
            g.request_args = request.args

    def ping_func(self):
        ping_msg = "Ping %s success. App run at %s" % (request.path, self.run_time)
        return jsonify({"status": self.config.get("MSG_STATUS", 2), "message": ping_msg})

    def __init__(self, import_name, **kwargs):
        self.blues = []
        super(Flask2, self).__init__(import_name, **kwargs)
        self.add_url_rule("/ping/", endpoint="app_ping", view_func=self.ping_func)
        self.before_request_funcs.setdefault(None, []).append(self._assign_default_g)
        self.before_request_funcs[None].append(self._packet_data)
        self.after_authorization_funcs = []

    def register_blues(self):
        for blue_item in self.blues:
            if hasattr(blue_item, "static_routes") is True:
                for rule_item in blue_item.static_routes:
                    self.add_url_rule2(rule_item)
            self.register_blueprint(blue_item)

    def add_blueprint(self, blue):
        blue.static_routes = UrlRules()
        self.blues.append(blue)

    def filter_user_agent(self, *accept_agent):
        fa = FilterUserAgent(self, *accept_agent)
        return fa

    def cross_domain(self):
        fc = FlaskCrossDomain(self)
        return fc

    def handle_30x(self):
        h = Handle30X(self)
        return h

    def real_ip(self, trust_proxy=None):
        if trust_proxy is None:
            trust_proxy = ["127.0.0.1"]
        r = RealIP(self, trust_proxy)
        return r
