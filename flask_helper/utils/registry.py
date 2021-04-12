# !/usr/bin/env python
# coding: utf-8
import collections
from flask_helper.exception import RepeatCallback

__author__ = 'zhouhenglc'


class DataRegistry(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_dict'):
            self._dict = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is not None:
            return cls._instance
        return cls()

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def set(self, key, value):
        self._dict[key] = value

    def set_default(self, key, default):
        if key not in self._dict:
            self._dict[key] = default
        return self._dict[key]

    def exist_in(self, key, value, add_not_exist=False):
        _values = self.get(key)
        if not _values:
            _values = []
        r = value in _values
        if not r and add_not_exist:
            self.append(key, value)
        return r

    def append(self, key, value):
        _values = self.get(key)
        if not _values:
            _values = []
        _values.append(value)
        self.set(key, _values)

    def update(self, key, **kwargs):
        _values = self.get(key)
        if not _values:
            _values = {}
        _values.update(**kwargs)
        self.set(key, _values)


class HookRegistry(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_dict'):
            self._dict = collections.defaultdict(dict)
            self._one_dict = collections.defaultdict(dict)

    @staticmethod
    def _get_id(callback):
        # TODO
        return callback.__name__

    @classmethod
    def get_instance(cls):
        if cls._instance is not None:
            return cls._instance
        return cls()

    def subscribe(self, callback, resource, event):
        callback_list = self._dict[resource].setdefault(event, [])
        callback_id = self._get_id(callback)
        for ck in callback_list:
            if callback_id == self._get_id(ck):
                return
        callback_list.append(callback)

    def notify(self, resource, event, trigger, **kwargs):
        callbacks = self._dict[resource].get(event, [])
        for callback in callbacks:
            callback(resource, event, trigger, **kwargs)

    def set_callback(self, callback, resource, event):
        if event in self._one_dict[resource]:
            raise RepeatCallback(resource, event)
        self._one_dict[resource][event] = callback

    def callback(self, resource, event, trigger, **kwargs):
        callback_fun = self._one_dict[resource].get(event, None)
        if callback_fun:
            return callback_fun(resource, event, trigger, **kwargs)


_HOOK = HookRegistry()
DATA_REGISTRY = DataRegistry()


def notify(resource, event, trigger, **kwargs):
    _HOOK.notify(resource, event, trigger, **kwargs)


def subscribe(callback, resource, event):
    return _HOOK.subscribe(callback, resource, event)


def subscribe_callback(*args):
    if len(args) == 2:
        resource = args[0]
        event = args[1]
    elif len(args) == 3:
        callback = args[0]
        resource = args[1]
        event = args[2]
        return _subscribe_callback(callback, resource, event)
    else:
        raise RuntimeError('require args: callback, resource, event')
    def decorator(f):
        subscribe_callback(f, resource, event)
        return f
    return decorator


def _subscribe_callback(callback, resource, event):
    return _HOOK.set_callback(callback, resource, event)


def notify_callback(resource, event,trigger, **kwargs):
    return _HOOK.callback(resource, event, trigger, **kwargs)
