#! /usr/bin/env python
# coding: utf-8

from flask import g, request, jsonify, make_response
from flask_helper.globals import remote_addr
from flask_helper.flask2 import Flask2
from flask_helper.utils.registry import DataRegistry



__author__ = 'meisanggou'

DATA = DataRegistry.get_instance()