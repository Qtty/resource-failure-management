#!/bin/bash

python init.py;

gunicorn --bind 0.0.0.0:5000 -m 007 wsgi:app;