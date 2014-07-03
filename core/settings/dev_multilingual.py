from .base import *

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

USE_MODELTRANSLATION = True

USE_I18N = True

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('es', _('Spanish'),
    ('fr', _('French'))),
    ('id', _('Indonesian')))

# Keep slugs etc. in English when generated automatically
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'

# Using a single translation.py in core for everything for now (rather than stick these in each app)
MODELTRANSLATION_TRANSLATION_FILES = (
    'core.translation',)
