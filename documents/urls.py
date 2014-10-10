from __future__ import unicode_literals

from django.conf.urls import patterns, url

import documents.views as views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.DocumentListView.as_view(), name='document-list'),
    url(r'^category/$', views.RootCategoriesView.as_view(), name='document-category-root'),
    url(r'^category/(?P<category_slugs>[\w/-]+)/$', views.CategoryView.as_view(), name='document-category'),
    url(r'^detail/(?P<slug>[-_\w]+)/$', views.DocumentDetailView.as_view(), name='document-detail'),
    url(r'^download/(?P<slug>[-_\w]+)/$', views.download, name='document-download'))
