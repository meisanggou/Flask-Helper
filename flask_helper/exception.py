# !/usr/bin/env python
# coding: utf-8


__author__ = 'zhouhenglc'


class InvalidHookClass(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Invalid FlaskHook Class'
