#! /usr/bin/env python
# coding: utf-8

from flask_helper import Flask2, g2

__author__ = '鹛桑够'


app = Flask2(__name__)


@app.route("/")
def index():
    print(g2)
    return "success"


if __name__ == "__main__":
    app.run()