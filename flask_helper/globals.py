# !/usr/bin/env python
# coding: utf-8
from contextvars import ContextVar
from werkzeug.local import LocalProxy

from flask.globals import _no_req_msg

__author__ = 'zhouhenglc'


unbound_message = _no_req_msg
_extra_req_ctx = ContextVar('flask_helper.extra_request_ctx')

extra_request_ctx = LocalProxy(_extra_req_ctx,
                               unbound_message=unbound_message)
request_id = LocalProxy(_extra_req_ctx, 'request_id',
                        unbound_message=unbound_message)
request_ip = LocalProxy(_extra_req_ctx, 'request_ip',
                     unbound_message=unbound_message)
user_no = LocalProxy(_extra_req_ctx, 'user_no',
                     unbound_message=unbound_message)
request_data = LocalProxy(_extra_req_ctx, 'request_data',
                          unbound_message=unbound_message)
db_session = LocalProxy(_extra_req_ctx, 'db_session',
                        unbound_message=unbound_message)
