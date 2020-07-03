# !/usr/bin/env python
# coding: utf-8
import logging

__author__ = 'zhouhenglc'

class DummyLog(object):

    def __init__(self):
        self.debug = self.info
        self.warning = self.warn = self.info
        self.error = self.info
        self.exception = self.critical = self.fatal = self.info

    def log(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass
