# !/usr/bin/env python
# coding: utf-8


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
