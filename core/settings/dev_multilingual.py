from .includes.common import *

DEBUG = True

# Make these unique, and don't share it with anybody.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs_multilingual",
        "USER": "cccs",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}

VIRTUALENV = 'cccs'

POSTGIS_VERSION = (2, 1, 2)