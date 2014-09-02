from __future__ import unicode_literals

from django.conf.urls import patterns, url

import projects.views as views

urlpatterns = patterns(
    '',
    url(r'^cccs/$',
        views.ProjectCCCSProjectListView.as_view(), name='project-list-cccs-tag'),
    url(r'^bycccstheme/$',
        views.ProjectCCCSThemeListView.as_view(), name='project-list-cccs-theme'),
    url(r'^bycccssector/$',
        views.ProjectCCCSSectorListView.as_view(), name='project-list-cccs-sector'),
    url(r'^bycccssubsector/(?P<pk>\d+)$',
        views.ProjectCCCSSubSectorListView.as_view(), name='project-list-cccs-subsector'),
    url(r'^cccs_sector_experience/$',
        views.ProjectCCCSSectorExperienceView.as_view(), name='project-experience-cccs-sector'),
    url(r'^byifcperformancestandard/$',
        views.ProjectIFCThemeListView.as_view(), name='project-list-ifc-theme'),
    url(r'^bycountry/$',
        views.ProjectCountryListView.as_view(), name='project-list-country'),
    url(r'^byifcsector/$',
        views.ProjectIFCSectorListView.as_view(), name='project-list-ifc-sector'),
    url(r'^project/(?P<slug>[-_\w]+)/$',
        views.ProjectDetailView.as_view(), name='project-detail'))
