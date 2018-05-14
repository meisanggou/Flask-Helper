# !/usr/bin/env python
# coding: utf-8

import os

__author__ = 'meisa'


def create_folder(folder_name, mode=0o777):
    if os.path.isdir(folder_name) is True:
        return True
    os.makedirs(folder_name, mode=mode)
    return True


def create_folder2(*folder_name, **kwargs):
    f = os.path.join(*folder_name)
    if os.path.isdir(f) is True:
        return f
    if "mode" in kwargs:
        mode = kwargs["mode"]
    else:
        mode = 0o777
    os.makedirs(f, mode=mode)
    return f
