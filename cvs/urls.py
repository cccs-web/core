from __future__ import unicode_literals

from django.conf.urls import patterns, url

import cvs.views as views

urlpatterns = patterns(
    '',

    url(r'^cv/(?P<slug>[-_\w]+)/$', views.CVDetailView.as_view(), name='cv-detail'),

    url(r'^project/bycccstheme/$', views.ProjectCCCSThemeListView.as_view(), name='project-list-cccs-theme'),
    url(r'^project/bycccssector/$', views.ProjectCCCSSectorListView.as_view(), name='project-list-cccs-sector'),
    url(r'^project/byifctheme/$', views.ProjectIFCThemeListView.as_view(), name='project-list-ifc-theme'),
    url(r'^project/bycountry/$', views.ProjectCountryListView.as_view(), name='project-list-country'),
    url(r'^project/byifcsector/$', views.ProjectIFCSectorListView.as_view(), name='project-list-ifc-sector'),
    url(r'^project/(?P<slug>[-_\w]+)/$', views.ProjectDetailView.as_view(), name='project-detail'))
