from __future__ import unicode_literals

from django.conf.urls import patterns, url

import documents.views as views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.DocumentListView.as_view(), name='document-list'),
    url(r'^detail/(?P<slug>[-_\w]+)/$', views.DocumentDetailView.as_view(), name='document-detail'),
    url(r'^download/(?P<slug>[-_\w]+)/$', views.download, name='document-download'))
