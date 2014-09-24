from django.db import models

from mezzanine.core.models import Displayable, RichText
from taggit.managers import TaggableManager


class Document(RichText, Displayable):
    source_file = models.FileField(upload_to='documents/%Y/%m/%d')
    creator = models.CharField(max_length=256, null=True, blank=True)
    tags = TaggableManager()
    search_fields = ("content", "title")
    # TODO: Add fields from Annex X1 spreadsheet
Document._meta.get_field('content').verbose_name = 'Description of content'
