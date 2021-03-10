#!/bin/sh
export FLASK_APP=app.py
export FLASK_DEBUG=0
source /opt/poof-web-scraper/my_env/bin/activate
gunicorn app:app -b :8080 --timeout 120 --workers=8 --threads=8 --worker-connections=1000
