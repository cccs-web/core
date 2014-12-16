from __future__ import unicode_literals

from django.conf.urls import patterns, url

import qgis.views as qv

urlpatterns = patterns(
    '',
    url(r'^$', qv.HomeView.as_view(), name='qgis-home'),
    url(r'^project/(?P<project_name>[\.-_\w]+)$', qv.QGISProjectView.as_view(), name='qgis-project'))
