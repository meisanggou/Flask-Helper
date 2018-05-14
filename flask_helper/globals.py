#! /usr/bin/env python
# coding: utf-8

from functools import partial
from werkzeug.local import LocalProxy
from flask.globals import _lookup_req_object

__author__ = '鹛桑够'


remote_addr = LocalProxy(partial(_lookup_req_object, 'remote_addr'))