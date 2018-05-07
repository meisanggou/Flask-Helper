#!/usr/bin/env bash
# python setup.py register -r pypi
python setup.py sdist --formats=gztar upload -r pypi
rm -rf *.egg-info
rm -rf dist
