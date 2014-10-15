from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

import documents.views as views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.DocumentListView.as_view(), name='document-list'),
    url(r'^category/$', views.RootCategoriesView.as_view(), name='document-category-root'),
    url(r'^category/(?P<category_slugs>[\w/-]+)/$', views.CategoryView.as_view(), name='document-category'),
    url(r'^detail/(?P<slug>[\w_-]+)/$', views.DocumentDetailView.as_view(), name='document-detail'),
    url(r'^bibtex/$$', TemplateView.as_view(template_name='documents/document_bibtex.html'), name='document-bibtex'),
    url(r'^download/(?P<slug>[\w_-]+)/$', views.download, name='document-download'))
