#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/cccs/.virtualenvs/test/bin/activate
source /home/cccs/.virtualenvs/test/bin/postactivate

cd /home/cccs/test

exec gunicorn -c /home/cccs/test/deploy/gunicorn.conf.py core.wsgi:application