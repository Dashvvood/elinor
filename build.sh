#!/bin/bash
rm -r build dist
python setup.py sdist bdist_wheel
twine upload ./dist/*
