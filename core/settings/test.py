from .includes.common import *

DEBUG = True

# Make these unique, and don't share it with anybody.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs_test",
        "USER": "cccs",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}


###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8174"
PROCESS_USER = 'cccs'
PROCESS_NAME = 'cccs_test'
SITE_TITLE = 'CCCS Test'
SITE_TAGLINE = None
VIRTUALENV = 'test'
