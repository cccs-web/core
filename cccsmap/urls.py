from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView

from mezzanine.conf import settings

import cccsmap

urlpatterns = patterns(
    '',
    url("^test/$", TemplateView.as_view(template_name='cccsmap/test.html'), name="maps_test"))
