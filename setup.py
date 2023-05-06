#! /usr/bin/env python
# coding: utf-8

#  __author__ = 'meisanggou'

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info <= (3, 7):
    sys.stderr.write("ERROR: flask_helper requires Python Version 3.7 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

name = "Flask-Helper"
version = "2.0.4"
url = "https://github.com/meisanggou/Flask-Helper"
license = "MIT"
author = "meisanggou"
short_description = "Flask Helper"
long_description = """Some Tools For Help You Use Flask"""
keywords = "flask_helper"
install_requires = ["Flask"]

setup(name=name,
      version=version,
      author=author,
      author_email="zhou5315938@163.com",
      url=url,
      packages=["flask_helper", "flask_helper/utils", 'flask_helper/hooks'],
      license=license,
      description=short_description,
      long_description=long_description,
      keywords=keywords,
      install_requires=install_requires
      )
