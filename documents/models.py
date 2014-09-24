from django.db import models

from mezzanine.core.models import Displayable, RichText
from taggit.managers import TaggableManager

import projects.models as pm


class BibTexEntryType(pm.UniqueNamed):
    pass


class CCCSEntryType(pm.UniqueNamed):
    pass


class Document(RichText, Displayable):
    source_file = models.FileField(upload_to='documents/%Y/%m/%d')
    author = models.CharField(max_length=256, null=True, blank=True)
    editor = models.CharField(max_length=256, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    chapter = models.CharField(max_length=256, null=True, blank=True)
    journal = models.CharField(max_length=256, null=True, blank=True)
    volume = models.CharField(max_length=256, null=True, blank=True)
    issue = models.CharField(max_length=256, null=True, blank=True)
    pages = models.CharField(max_length=256, null=True, blank=True)
    series = models.CharField(max_length=256, null=True, blank=True)
    language = models.CharField(max_length=256, null=True, blank=True)
    publisher = models.CharField(max_length=256, null=True, blank=True)
    institution = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    cccs_source_path = models.CharField(max_length=512, null=True, blank=True)
    bibtex_entry_type = models.ForeignKey(BibTexEntryType, null=True, blank=True)
    cccs_entry_type = models.ForeignKey(CCCSEntryType, null=True, blank=True)
    countries = models.ManyToManyField(pm.Country, related_name='documents', verbose_name="Country / Countries")
    tags = TaggableManager(blank=True)

    search_fields = ("content", "title")

Document._meta.get_field('content').verbose_name = 'Description of content'
