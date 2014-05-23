from __future__ import unicode_literals

from django.conf.urls import patterns, url

import cvs.views as views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.CVListView.as_view(), name='cv-list'),
    url(r'^cv/detail/(?P<slug>[-_\w]+)/$', views.CVDetailView.as_view(), name='cv-detail'),
    url(r'^cv/update/(?P<slug>[-_\w]+)/$', views.CVUpdateView.as_view(), name='cv-update'))
