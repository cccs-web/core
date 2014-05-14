from __future__ import unicode_literals

from django.conf.urls import patterns, url

import cvs.views as views

urlpatterns = patterns(
    '',
    url(r'^project/list/$', views.ProjectListView.as_view(), name='project-list'),
    url(r'^project/(?P<slug>[-_\w]+)/$', views.ProjectDetailView.as_view(), name='project-detail'))
