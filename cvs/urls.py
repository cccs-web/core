from __future__ import unicode_literals

from django.conf.urls import patterns, url

import cvs.views as views

urlpatterns = patterns(
    '',
    url(r'^cv/(?P<slug>[-_\w]+)/$', views.CVDetailView.as_view(), name='cv-detail'))
