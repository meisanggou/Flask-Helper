# !/usr/bin/env python
# coding: utf-8
import os
import sys

import logging
from logging import Formatter, StreamHandler
from logging.handlers import WatchedFileHandler


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


LOG_LEVEL = logging.INFO
LOG_FILE = None

fmt = Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = None

console_handle = StreamHandler(sys.stdout)
console_handle.level = logging.DEBUG
console_handle.setFormatter(fmt)


def set_logger_as_root(name):
    logger = logging.getLogger(name)
    if file_handler:
        logger.addHandler(file_handler)
    elif os.environ.get('LOG_FILE'):
        set_log_file(os.environ.get('LOG_FILE'))
        logger.addHandler(file_handler)
    else:
        logger.addHandler(console_handle)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    return logger


def getLogger(name=None):
    set_logger_as_root(name)
    logger = logging.getLogger(name)
    return logger


def set_log_file(log_file):
    global file_handler
    file_handler = WatchedFileHandler(log_file)
    file_handler.level = logging.DEBUG
    file_handler.setFormatter(fmt)
