#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/webcore/.virtualenvs/staging/bin/activate
source /home/webcore/.virtualenvs/staging/bin/postactivate

cd /home/webcore/staging

exec gunicorn -c /home/webcore/staging/deploy/gunicorn.conf.py core.wsgi:application