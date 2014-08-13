from .includes.common import *

DEBUG = True

# Make these unique, and don't share it with anybody.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs_staging",
        "USER": "cccs",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}


###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8200"
PROCESS_USER = 'cccs'
PROCESS_NAME = 'cccs_staging'
SITE_TITLE = 'CCCS Staging'
SITE_TAGLINE = None
VIRTUALENV = 'cccs'
