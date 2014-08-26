#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/cristi/.virtualenvs/cccs/bin/activate
source /home/cristi/.virtualenvs/cccs/bin/postactivate

cd /home/cristi/cccs

exec gunicorn -c /home/cristi/cccs/deploy/gunicorn.conf.py core.wsgi:application