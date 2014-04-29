#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/webcore/.virtualenvs/production/bin/activate
source /home/webcore/.virtualenvs/production/bin/postactivate

cd /home/webcore/production

exec gunicorn -c /home/webcore/production/_deploy/gunicorn.conf.py core.wsgi:application