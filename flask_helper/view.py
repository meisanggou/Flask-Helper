# !/usr/bin/env python
# coding: utf-8
from contextlib import contextmanager
import functools

from flask import Blueprint
from flask import g
from flask import jsonify
from flask import Response


__author__ = 'zhouhenglc'


@contextmanager
def _context_func(*args):
    yield None


class View(Blueprint):
    jinja_env = {}
    view_context_func = _context_func

    def register_jinja_global_env(self, key, value):
        self.jinja_env[key] = value

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func:
            @functools.wraps(view_func)
            def inner(*args, **kwargs):
                with self.view_context_func() as context:
                    g.context = context
                    r = view_func(*args, **kwargs)
                    if isinstance(r, Response):
                        return r
                    if isinstance(r, dict):
                        return jsonify(r)

                    return r
            Blueprint.add_url_rule(self, rule, endpoint, inner, **options)
        else:
            Blueprint.add_url_rule(self, rule, endpoint, view_func, **options)
