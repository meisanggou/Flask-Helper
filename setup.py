#! /usr/bin/env python
# coding: utf-8

#  __author__ = 'meisanggou'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info <= (2, 7):
    sys.stderr.write("ERROR: jingyun flask requires Python Version 2.7 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

name = "Flask-Helper"
version = "0.1"
url = "https://github.com/meisanggou/Flask-Helper"
license = "MIT"
author = "meisanggou"
short_description = "Flask Helper"
long_description = """Some Tools For Help You Use Flask"""
keywords = "Flask-Helper"
install_requires = ["Flask"]

setup(name=name,
      version=version,
      author=author,
      author_email="zhouheng@gene.ac",
      url=url,
      packages=["Flask-Helper"],
      license=license,
      description=short_description,
      long_description=long_description,
      keywords=keywords,
      install_requires=install_requires
      )
