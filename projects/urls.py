from __future__ import unicode_literals

from django.conf.urls import patterns, url

import projects.views as views

urlpatterns = patterns(
    '',
    url(r'^bycccstheme/$', views.ProjectCCCSThemeListView.as_view(), name='project-list-cccs-theme'),
    url(r'^bycccssector/$', views.ProjectCCCSSectorListView.as_view(), name='project-list-cccs-sector'),
    url(r'^byifctheme/$', views.ProjectIFCThemeListView.as_view(), name='project-list-ifc-theme'),
    url(r'^bycountry/$', views.ProjectCountryListView.as_view(), name='project-list-country'),
    url(r'^byifcsector/$', views.ProjectIFCSectorListView.as_view(), name='project-list-ifc-sector'),
    url(r'^project/(?P<slug>[-_\w]+)/$', views.ProjectDetailView.as_view(), name='project-detail'))
