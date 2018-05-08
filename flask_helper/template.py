#! /usr/bin/env python
# coding: utf-8

from flask import render_template

__author__ = '鹛桑够'


class RenderTemplate(object):

    def __init__(self, template_dir="", **kwargs):
        self.template_dir = template_dir
        self.kwargs = kwargs

    def render(self, template_name_or_list, **context):
        if self.template_dir != "":
            template_name_or_list = "%s/%s" % (self.template_dir, template_name_or_list)
        self.kwargs.update(context)
        return render_template(template_name_or_list, **self.kwargs)