# !/usr/bin/env python
# coding: utf-8
import functools

from flask import Blueprint, Response, jsonify

__author__ = 'zhouhenglc'


class View(Blueprint):
    jinja_env = {}

    def register_jinja_global_env(self, key, value):
        self.jinja_env[key] = value

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func:
            @functools.wraps(view_func)
            def inner(*args, **kwargs):
                r = view_func(*args, **kwargs)
                if isinstance(r, Response):
                    return r
                if isinstance(r, dict):
                    return jsonify(r)

                return r
            Blueprint.add_url_rule(self, rule, endpoint, inner, **options)
        else:
            Blueprint.add_url_rule(self, rule, endpoint, view_func, **options)
