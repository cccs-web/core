from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import VillageView

urlpatterns = patterns(
    '',
    url("^test/$", TemplateView.as_view(template_name='cccsmap/test.html'), name="maps_test"),
    url("^villages/$", VillageView.as_view(), name="villages"))
