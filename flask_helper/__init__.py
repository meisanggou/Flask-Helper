#! /usr/bin/env python
# coding: utf-8

from flask import g, request, jsonify, make_response
from globals import remote_addr
from flask2 import Flask2
from cross_domain import FlaskCrossDomain
from template import RenderTemplate
from upload import support_upload, support_upload2


__author__ = 'meisanggou'
