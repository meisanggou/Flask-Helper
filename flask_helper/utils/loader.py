# !/usr/bin/env python
# coding: utf-8
from functools import partial
import importlib.util
import inspect
import os
import re
import sys

__author__ = 'zhouhenglc'


_SEPARATOR_REGEX = re.compile(r'[/\\]+')


def _is_subclass(cls_type, cls):
    if not inspect.isclass(cls):
        return False
    return issubclass(cls, cls_type)


def _is_instance(obj_type, obj):
    return isinstance(obj, obj_type)


def load_classes(module_prefix, file_path, cls_type):
    base_name = os.path.basename(os.path.splitext(file_path)[0])
    if file_path.endswith('.so'):
        base_name = base_name.rsplit('.', 1)[0]
    module_name = '.'.join([module_prefix, base_name])
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if module_name not in sys.modules:
        sys.modules[module_name] = module
    spec.loader.exec_module(module)
    _func = partial(_is_subclass, cls_type)
    classes = inspect.getmembers(module, _func)
    r_classes = []
    for _class in classes:
        if _class[1].__module__ == module_name:
            r_classes.append(_class[1])
    return r_classes


def load_objects(module_prefix, file_path, obj_type):
    base_name = os.path.basename(os.path.splitext(file_path)[0])
    if file_path.endswith('.so'):
        base_name = base_name.rsplit('.', 1)[0]
    module_name = '.'.join([module_prefix, base_name])
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if module_name not in sys.modules:
        sys.modules[module_name] = module
    spec.loader.exec_module(module)
    _func = partial(_is_instance, obj_type)
    objects = inspect.getmembers(module, _func)
    r_objects = []
    for _obj in objects:
        r_objects.append(_obj[1])
    return r_objects


def load_classes_from_directory(top_dir, module_prefix, cls_type,
                                ignore_error=True, file_suffix='.py'):
    top_dir = os.path.abspath(top_dir)
    top_len = len(top_dir)
    classes = []
    for root, dirs, files in os.walk(top_dir):
        for _file in files:
            if not  _file.endswith(file_suffix):
                continue
            _sub_m = _SEPARATOR_REGEX.sub('.', root[top_len:]).split('.')
            _sub_m_l = [x for x in _sub_m if x.strip()]
            mp = '.'.join([module_prefix, ] + _sub_m_l)
            _classes = load_classes(mp, os.path.join(root, _file), cls_type)
            classes.extend(_classes)
    return classes


def load_objects_from_directory(top_dir, module_prefix, obj_type,
                                ignore_error=True, file_suffix='.py'):
    top_dir = os.path.abspath(top_dir)
    top_len = len(top_dir)
    objects = []
    for root, dirs, files in os.walk(top_dir):
        for _file in files:
            if not  _file.endswith(file_suffix):
                continue
            _sub_m = _SEPARATOR_REGEX.sub('.', root[top_len:]).split('.')
            _sub_m_l = [x for x in _sub_m if x.strip()]
            mp = '.'.join([module_prefix, ] + _sub_m_l)
            _objects = load_objects(mp, os.path.join(root, _file), obj_type)
            objects.extend(_objects)
    return list(set(objects))


if __name__ == '__main__':
    from flask_helper.flask_hook import FlaskHook
    load_classes_from_directory(r'../../flask_helper', 'flask_helper.ex_hooks', FlaskHook)
