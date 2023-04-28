# !/usr/bin/env python
# coding: utf-8

from itsdangerous import BadSignature
try:
    from flask.helpers import total_seconds
except ImportError:
    total_seconds = None
from flask.sessions import SecureCookieSessionInterface
from flask import g

__author__ = 'meisa'


class SecureCookieSessionInterface2(SecureCookieSessionInterface):

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(self.get_cookie_name(app))
        header_cookie = request.headers.get("X-COOKIE-%s" % self.get_cookie_name(app).upper())
        if not val and not header_cookie:
            return self.session_class()
        if hasattr(app.permanent_session_lifetime, 'total_seconds'):
            max_age = int(app.permanent_session_lifetime.total_seconds())
        else:
            max_age = total_seconds(app.permanent_session_lifetime)
        session_data = dict()
        if val is not None:
            try:
                data = s.loads(val, max_age=max_age)
                session_data.update(data)
            except BadSignature:
                return self.session_class()
        if header_cookie is not None:
            try:
                data2 = s.loads(header_cookie, max_age=max_age)
                session_data.update(data2)
            except BadSignature:
                pass
        sc = self.session_class(session_data)
        return sc

    def get_expiration_time(self, app, session):
        if "permanent_session" in session and session["permanent_session"] is True:
            return None
        if "permanent_session" in g and g.permanent_session is True:
            return None
        SecureCookieSessionInterface.get_expiration_time(self, app, session)

    def save_session(self, app, session, response):
        SecureCookieSessionInterface.save_session(self, app, session, response)
        # val = self.get_signing_serializer(app).dumps(dict(session))
        # response.headers["X-COOKIE-%s" % app.session_cookie_name.upper()] = val