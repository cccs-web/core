import hashlib
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from mezzanine.core.models import Displayable, RichText, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from taggit.managers import TaggableManager

from storages.backends.s3boto import S3BotoStorage

import projects.models as pm
from categories.base import (MPTTModel,
                             TreeForeignKey,
                             CategoryManager,
                             TreeManager,
                             slugify,
                             SLUG_TRANSLITERATOR,
                             force_unicode)


def sha1(f):
    sha = hashlib.sha1()
    for line in f:
        sha.update(line)
    return sha.hexdigest()


class DocumentCategory(MPTTModel):
    """
    Largely a copy of categories.models.CategoryBase because we needed bigger fields.
    Refactor with own django-categories/pull request if we have to do more with this :(
    """
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            related_name='children',
                            verbose_name=_('parent'))
    name = models.CharField(max_length=512, verbose_name=_('name'))
    slug = models.SlugField(max_length=512, verbose_name=_('slug'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    objects = CategoryManager()
    tree = TreeManager()

    def save(self, *args, **kwargs):
        """
        While you can activate an item without activating its descendants,
        It doesn't make sense that you can deactivate an item and have its
        decendants remain active.
        """
        if not self.slug:
            self.slug = slugify(SLUG_TRANSLITERATOR(self.name))[:50]

        super(DocumentCategory, self).save(*args, **kwargs)

        if not self.active:
            for item in self.get_descendants():
                if item.active != self.active:
                    item.active = self.active
                    item.save()

    def __unicode__(self):
        ancestors = self.get_ancestors()
        return ' > '.join([force_unicode(i.name) for i in ancestors] + [self.name, ])

    class Meta:
        unique_together = ('parent', 'name')
        ordering = ('tree_id', 'lft')
        verbose_name_plural = 'document categories'

    class MPTTMeta:
        order_insertion_by = 'name'


class BibTexEntryType(pm.UniqueNamed):
    class Meta:
        verbose_name = 'BIBTEX Entry Type'
        verbose_name_plural = 'BIBTEX Entry Types'


class CCCSEntryType(pm.UniqueNamed):
    class Meta:
        verbose_name = 'CCCS Entry Type'
        verbose_name_plural = 'CCCS Entry Types'


class Document(RichText, Displayable):
    source_file = models.FileField(max_length=512, upload_to='documents/%Y/%m/%d', storage=S3BotoStorage())
    original_source_filename = models.CharField(max_length=256, null=True, blank=True)
    sha = models.CharField(max_length=40, null=True, blank=True)
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
    categories = models.ManyToManyField(DocumentCategory, related_name='documents')

    search_fields = ("content", "title", "tags__name")

    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse("document-detail", args=(self.slug,))

    @property
    def tag_string(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    def update_sha(self):
        self.source_file.open()
        try:
            self.sha = sha1(self.source_file)
        finally:
            self.source_file.close()

Document._meta.get_field('content').verbose_name = 'Description of content'
