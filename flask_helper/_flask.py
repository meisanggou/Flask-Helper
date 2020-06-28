# !/usr/bin/env python
# coding: utf-8
from flask import Flask
import os

from flask_helper.exception import InvalidHookClass
from flask_helper.flask_hook import FlaskHook
from flask_helper.hooks.cors_hook import CorsHook
from flask_helper.hooks.handle_30x_hook import Handle30xHook
from flask_helper.hooks.real_ip_hook import RealIPHook
from flask_helper.hooks.user_agent_hook import UserAgentHook
from flask_helper.view import View

from flask_helper.utils.loader import load_classes_from_directory
from flask_helper.utils.loader import load_objects_from_directory

__author__ = 'zhouhenglc'


class _HookFlask(object):

    def __init__(self):
        self.hooks = []

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


class PredefinedHookFlask(_HookFlask):
    def cross_domain(self, **kwargs):
        hook_obj = self.add_hook(CorsHook, **kwargs)
        return hook_obj

    def filter_user_agent(self, *args):
        hook_obj = self.add_hook(UserAgentHook, *args)
        return hook_obj

    def handle_30x(self, **kwargs):
        hook_obj = self.add_hook(Handle30xHook, **kwargs)
        return hook_obj

    def real_ip(self, trust_proxy=None):
        if trust_proxy is None:
            trust_proxy = ["127.0.0.1"]
        hook_obj = self.add_hook(RealIPHook, trust_proxy=trust_proxy)
        return hook_obj


class FlaskHelper(Flask, PredefinedHookFlask):

    def __init__(self, import_name, *args, **kwargs):
        Flask.__init__(self, import_name, *args, **kwargs)
        PredefinedHookFlask.__init__(self)
        self.before_request_funcs.setdefault(None, [])
        self.after_request_funcs.setdefault(None, [])
        self.before_request_funcs[None].append(self.before_request_hook)
        self.after_request_funcs[None].append(self.after_request_hook)

        self.hooks_folders = set()
        default_hooks_folder = os.path.join(self.root_path, 'hooks')
        if os.path.exists(default_hooks_folder):
            self.register_hooks(default_hooks_folder)

        self.views_folders = set()
        default_views_folder = os.path.join(self.root_path, 'views')
        if os.path.exists(default_views_folder):
            self.register_views(default_views_folder)

    def register_blueprint(self, blueprint, **options):
        if isinstance(blueprint, View):
            self.jinja_env.globals.update(blueprint.jinja_env)
        Flask.register_blueprint(self, blueprint, **options)

    def register_views(self, views_folder):
        views_folder = os.path.abspath(views_folder)
        if views_folder in self.views_folders:
            return
        self.views_folders.add(views_folder)
        module_prefix = 'flask_helper.views_%s' % len(self.hooks_folders)
        v_objects = load_objects_from_directory(views_folder, module_prefix,
                                                View)
        for v_obj in v_objects:
            self.register_blueprint(v_obj)

    def register_hooks(self, hooks_folder):
        hooks_folder = os.path.abspath(hooks_folder)
        if hooks_folder in self.hooks_folders:
            return
        self.hooks_folders.add(hooks_folder)
        module_prefix = 'flask_helper.hooks_%s' % len(self.hooks_folders)
        h_classes = load_classes_from_directory(hooks_folder, module_prefix,
                                                FlaskHook)
        for h_class in h_classes:
            self.add_hook(h_class)

    def run(self, host=None, port=None, **options):
        log = options.pop('log', None)
        try:
            import eventlet
            from eventlet import wsgi
            eventlet.monkey_patch()
            if host is None:
                host = '0.0.0.0'
            if port is None:
                port = 5000
            listen = eventlet.listen((host, port))
            wsgi.server(listen, self, log=log, **options)
        except ImportError:
            Flask.run(host, port, **options)
