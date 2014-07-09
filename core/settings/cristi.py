from .includes.common import *

DEBUG = True

# Make these unique, and don't share it with anybody.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs",
        "USER": "cccs",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}

VIRTUALENV = 'cccs'

###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8000"
PROCESS_USER = 'cristi'
PROCESS_NAME = 'cristi_cccs'
SITE_TITLE = "Cristi's CCCS"
SITE_TAGLINE = None
VIRTUALENV = 'cccs'