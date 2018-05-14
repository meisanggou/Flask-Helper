#! /usr/bin/env python
# coding: utf-8

from functools import partial
from werkzeug.local import LocalProxy
from flask.globals import _lookup_req_object

__author__ = '鹛桑够'


g2 = LocalProxy(partial(_lookup_req_object, 'g2'))