#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/cccs/.virtualenvs/staging/bin/activate
source /home/cccs/.virtualenvs/staging/bin/postactivate

cd /home/cccs/staging

exec gunicorn -c /home/cccs/staging/deploy/gunicorn.conf.py core.wsgi:application