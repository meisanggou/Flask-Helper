#!/usr/bin/env bash
# python setup.py register -r pypi
python setup.py sdist --formats=gztar
twine upload dist/*
rm -rf *.egg-info
rm -rf dist
