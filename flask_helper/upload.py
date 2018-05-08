#! /usr/bin/env python
# coding: utf-8

import os
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, Blueprint, send_from_directory, request, jsonify, url_for

__author__ = '鹛桑够'


def support_upload(app_or_blue, upload_route="upload", get_route="file", static_folder=None):
    if isinstance(app_or_blue, (Flask, Blueprint)) is Flask:
        raise RuntimeError("only support Flask or Blueprint object")

    if static_folder is None:
        if not app_or_blue.has_static_folder:
            raise RuntimeError('No static folder for this object')
        static_folder = app_or_blue.static_folder

    def get_upload(filename):
        cache_timeout = app_or_blue.get_send_file_max_age(filename)
        return send_from_directory(static_folder, filename, cache_timeout=cache_timeout)

    get_endpoint = "%s_get_upload" % get_route
    app_or_blue.add_url_rule("/" + get_route + '/<path:filename>', endpoint=get_endpoint, view_func=get_upload)

    get_endpoint = "%s.%s" % (app_or_blue.name, get_endpoint)

    @app_or_blue.route("/" + upload_route + "/", methods=["POST"])
    def handle_upload():
        r = dict()
        for key in request.files:
            file_item = request.files[key]
            filename = secure_filename(file_item.filename)
            extension = filename.rsplit(".", 1)[-1].lower()
            save_name = uuid.uuid4().hex + ".%s" % extension
            file_item.save(os.path.join(static_folder, save_name))
            r[key] = url_for(get_endpoint, filename=save_name)
        return jsonify({"status": True, "data": r})
