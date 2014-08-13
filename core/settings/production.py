from .includes.common import *

DEBUG = False

# Make these unique, and don't share it with anybody.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs",
        "USER": "cccs",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}


###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8000"
PROCESS_USER = 'cccs'
PROCESS_NAME = 'cccs_production'
SITE_TITLE = 'Cross-Cultural Consulting Services'
SITE_TAGLINE = None
VIRTUALENV = 'cccs'
