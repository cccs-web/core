
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "xxxxxxxxxxxxxxxxx"
NEVERCACHE_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cccs",
        "USER": "cccs",
        "PASSWORD": "xxxxxxxxx",
        "HOST": "",
        "PORT": ""}}

VIRTUALENV = 'cccs'
