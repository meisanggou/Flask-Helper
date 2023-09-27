#! /usr/bin/env python
# coding: utf-8

from flask.ctx import RequestContext

__author__ = '鹛桑够'


class RequestContext2(RequestContext):

    def __init__(self, app, environ, request=None):
        RequestContext.__init__(self, app, environ, request)
        self.remote_addr = self.request.remote_addr


class ExtraRequestContext(object):

    def __init__(self):
        self.request_id = ''
        self.user_no = ''
        self.db_session = ''
        self.request_ip = ''
        self.request_data = {}

    def set_value(self, key, value):
        setattr(self, key, value)
