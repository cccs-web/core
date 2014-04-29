#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/webcore/.virtualenvs/pwc/bin/activate
source /home/webcore/.virtualenvs/pwc/bin/postactivate

cd /home/webcore/core

exec gunicorn -c /home/webcore/core/_deploy/gunicorn.conf.py wsgi:application