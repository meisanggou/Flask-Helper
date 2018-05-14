#! /usr/bin/env python
# coding: utf-8

from flask_helper import Flask2

__author__ = '鹛桑够'


app = Flask2(__name__)
app.cross_domain()
app.filter_user_agent()
app.handle_30x()


@app.route("/")
def index():
    return "success"


if __name__ == "__main__":
    app.run()