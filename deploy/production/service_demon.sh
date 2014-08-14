#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/cccs/.virtualenvs/production/bin/activate
source /home/cccs/.virtualenvs/production/bin/postactivate

cd /home/cccs/production

exec gunicorn -c /home/cccs/production/deploy/gunicorn.conf.py core.wsgi:application