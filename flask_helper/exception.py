# !/usr/bin/env python
# coding: utf-8


__author__ = 'zhouhenglc'


class InvalidHookClass(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Invalid FlaskHook Class'


class RequestException(Exception):
    code = 500
    message = ''

    def __init__(self, detail=None, *args, **kwargs):
        self.msg = self.message % kwargs
        if detail is None:
            self.detail = self.msg
        else:
            self.detail = detail
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        _str = 'msg: %s, detail: %s' % (self.msg, self.detail)
        return _str
