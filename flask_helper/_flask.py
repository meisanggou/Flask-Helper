# !/usr/bin/env python
# coding: utf-8
from flask import Flask
from flask_helper.exception import InvalidHookClass
from flask_helper.flask_hook import FlaskHook
from flask_helper.hooks.cors_hook import CorsHook
from flask_helper.hooks.handle_30x_hook import Handle30xHook
from flask_helper.hooks.user_agent_hook import UserAgentHook

__author__ = 'zhouhenglc'


class FlaskHelper(Flask):

    def __init__(self, import_name, *args, **kwargs):
        Flask.__init__(self, import_name, *args, **kwargs)
        self.hooks = []
        self.before_request_funcs.setdefault(None, [])
        self.after_request_funcs.setdefault(None, [])
        self.before_request_funcs[None].append(self.before_request_hook)
        self.after_request_funcs[None].append(self.after_request_hook)

    def before_request_hook(self):
        for hook in self.hooks:
            resp = hook.before_request()
            if resp is not None:
                return resp

    def after_request_hook(self, response):
        for hook in reversed(self.hooks):
            response = hook.after_request(response)
        return response

    def add_hook(self, hook_cls, *args, **kwargs):
        if not issubclass(hook_cls, FlaskHook):
            raise InvalidHookClass()
        hook_obj = hook_cls(self, *args, **kwargs)
        insert_i = len(self.hooks)
        for i in range(len(self.hooks) - 1, -1, -1):
            if type(self.hooks[i]) == hook_cls:
                return self.hooks[i]
            if hook_obj.priority < self.hooks[i].priority:
                insert_i = i
        self.hooks.insert(insert_i, hook_obj)
        return hook_obj

    def cross_domain(self, **kwargs):
        hook_obj = self.add_hook(CorsHook, **kwargs)
        return hook_obj

    def filter_user_agent(self, *args):
        hook_obj = self.add_hook(UserAgentHook, *args)
        return hook_obj

    def handle_30x(self, **kwargs):
        hook_obj = self.add_hook(Handle30xHook, **kwargs)
        return hook_obj
