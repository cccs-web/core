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
                             SLUG_TRANSLITERATOR,  # Showing incorrect because of PyCharm bug
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
        return '/'.join([force_unicode(i.name) for i in ancestors] + [self.name, ])

    class Meta:
        unique_together = ('parent', 'name')
        ordering = ('tree_id', 'lft')
        verbose_name_plural = 'document categories'

    class MPTTMeta:
        order_insertion_by = 'name'

    def get_absolute_url(self):
        return reverse("document-category", args=('/'.join(self.category_slugs),))

    @property
    def category_slugs(self):
        category_slugs = [self.slug]
        parent = self.parent
        while parent:
            category_slugs.insert(0, parent.slug)
            parent = parent.parent
        return category_slugs


class BibTexEntryType(pm.UniqueNamed):
    class Meta:
        verbose_name = 'BIBTEX Entry Type'
        verbose_name_plural = 'BIBTEX Entry Types'


class CCCSEntryType(pm.UniqueNamed):
    class Meta:
        verbose_name = 'CCCS Entry Type'
        verbose_name_plural = 'CCCS Entry Types'


class Url(pm.UniqueNamed):
    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"

Url._meta.get_field('name').verbose_name = 'URL String'


class FileName(pm.UniqueNamed):
    pass


class Author(pm.UniqueNamed):
    class Meta:
        verbose_name = 'Author(s)'
        verbose_name_plural = 'Author(s)'


class Editor(pm.UniqueNamed):
    class Meta:
        verbose_name = 'Editor(s)'
        verbose_name_plural = 'Editor(s)'


class Document(RichText, Displayable):
    source_file = models.FileField(max_length=512, upload_to='documents/%Y/%m/%d', storage=S3BotoStorage())
    sha = models.CharField(max_length=40, null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='documents')
    editors = models.ManyToManyField(Editor, related_name='documents')
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    chapter = models.CharField(max_length=256, null=True, blank=True)
    journal = models.CharField(max_length=256, null=True, blank=True)
    volume = models.CharField(max_length=256, null=True, blank=True)
    issue = models.CharField(max_length=256, null=True, blank=True)
    pages = models.CharField(max_length=256, null=True, blank=True)
    series = models.CharField(max_length=256, null=True, blank=True)
    language = models.CharField(max_length=256, null=True, blank=True)
    publishing_agency = models.CharField(max_length=256, null=True, blank=True)
    publishing_house = models.CharField(max_length=256, null=True, blank=True)
    publisher_city = models.CharField(max_length=256, null=True, blank=True)
    publisher_address = models.CharField(max_length=256, null=True, blank=True)
    cccs_source_path = models.CharField(max_length=512, null=True, blank=True)
    bibtex_entry_type = models.ForeignKey(BibTexEntryType, null=True, blank=True)
    cccs_entry_type = models.ForeignKey(CCCSEntryType, null=True, blank=True)
    countries = models.ManyToManyField(pm.Country, related_name='documents', verbose_name="Country / Countries")
    tags = TaggableManager(blank=True)
    categories = models.ManyToManyField(DocumentCategory, related_name='documents')
    url = models.ManyToManyField(Url, related_name='documents')
    date_received = models.DateField(null=True, blank=True)
    receiving_team_member = models.CharField(max_length=128, null=True, blank=True)
    filenames = models.ManyToManyField(FileName, related_name='documents')
    regions = models.CharField(verbose_name='Region(s)', max_length=128, null=True, blank=True)
    document_id = models.CharField(verbose_name='Doc ID#/ISSN/ISBN', max_length=128, null=True, blank=True)
    annotation = models.CharField(verbose_name='Bibliographic annotation', max_length=128, null=True, blank=True)
    notes = models.TextField(verbose_name='Reviewer Notes', null=True, blank=True)

    search_fields = ("content", "title", "tags__name")

    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse("document-detail", args=(self.slug,))

    @property
    def tag_string(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    def update_sha(self):
        try:
            self.source_file.open()
            try:
                self.sha = sha1(self.source_file)
            finally:
                self.source_file.close()
        except IOError:
            self.sha = 'file missing'

Document._meta.get_field('content').verbose_name = 'Abstract/Description of content'


def categories_from_slugs(slugs):
    parent = None
    result = list()
    for slug in slugs:
        category = DocumentCategory.objects.get(slug=slug, parent=parent)
        result.append(category)
        parent = category
    return result


def verify_categories(category_names, create_if_absent=False):
    """
    Create the category_names ancestral tree if it does not already exist
    :param category_names: list of category names with root at the top
    :return: list of the actual categories corresponding to the names.
    """
    parent = None
    result = list()
    for category_name in category_names:
        try:
            category = DocumentCategory.objects.get(
                name=category_name,
                parent=parent)
        except DocumentCategory.DoesNotExist:
            if create_if_absent:
                category = DocumentCategory(
                    name=category_name,
                    parent=parent)
                category.save()
            else:
                raise
        result.append(category)
        parent = category
    return result


def get_root_categories():
    return DocumentCategory.tree.root_nodes()


def get_orphan_documents():
    return Document.objects.filter(categories=None)