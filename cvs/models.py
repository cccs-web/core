from django.db import models
from django.core.urlresolvers import reverse

from mezzanine.utils.urls import unique_slug, slugify


class CCCSModel(models.Model):
    class Meta:
        abstract = True

    @property
    def meta(self):
        return self._meta


class HasProjectsMixin(object):

    @property
    def project_count(self):
        return self.projects.count()


class UniqueNamed(CCCSModel):
    name = models.CharField(max_length=512, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


class UniqueNamedWithSlug(UniqueNamed):
    slug = models.CharField(max_length=2000, blank=True, null=True,
                            help_text="Leave blank to have the slug (url) auto-generated from "
                                      "the title.")

    class Meta(UniqueNamed.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        """
        If no slug is provided, generates one before saving.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(UniqueNamedWithSlug, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to
        utils.urls.unique_slug, which appends an index if necessary.
        """
        # For custom content types, use the ``Page`` instance for
        # slug lookup.
        slug_qs = self.__class__.objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """
        return slugify(self.name)


class Country(HasProjectsMixin, UniqueNamed):
    """
    There are lots of unique indexes here; the table is often used and rarely updated.
    """
    iso_english_name = models.CharField(max_length=80, unique=True)
    fips = models.CharField(max_length=2, null=True, blank=True)
    iso_numeric = models.IntegerField(null=True, blank=True)
    iso_3166 = models.CharField(max_length=3, null=True, blank=True)
    iso = models.CharField(max_length=7, null=True, blank=True)
    notes = models.TextField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.iso)


class CCCSTheme(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Theme'
        verbose_name_plural = 'CCCS Themes'

    @property
    def projects(self):
        return Project.objects.filter(cccs_subthemes__theme=self)


class CCCSSubTheme(HasProjectsMixin, CCCSModel):
    name = models.CharField(max_length=512)
    theme = models.ForeignKey(CCCSTheme, related_name='subtheme_set')

    class Meta:
        verbose_name = 'CCCS SubTheme'
        verbose_name_plural = 'CCCS SubThemes'
        ordering = ['name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.name, self.name)


class CCCSSector(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Sector'
        verbose_name_plural = 'CCCS Sectors'

    @property
    def projects(self):
        return Project.objects.filter(cccs_subsectors__sector=self)


class CCCSSubSector(HasProjectsMixin, CCCSModel):
    name = models.CharField(max_length=512)
    sector = models.ForeignKey(CCCSSector, related_name='sub_themes')

    class Meta:
        verbose_name = 'CCCS SubSector'
        verbose_name_plural = 'CCCS SubSectors'
        ordering = ['name']
        unique_together = ('sector', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.sector.name, self.name)


class IFCTheme(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Theme'
        verbose_name_plural = 'IFC Themes'

    @property
    def projects(self):
        return Project.objects.filter(ifc_subthemes__theme=self)


class IFCSubTheme(HasProjectsMixin, CCCSModel):
    name = models.CharField(max_length=512)
    theme = models.ForeignKey(IFCTheme, related_name='sub_themes')

    class Meta:
        verbose_name = 'IFC SubTheme'
        verbose_name_plural = 'IFC SubThemes'
        ordering = ['name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.name, self.name)


class IFCSector(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Sector'
        verbose_name_plural = 'IFC Sectors'


class Project(UniqueNamedWithSlug):
    date_range = models.CharField(help_text="Deprecate and copy values into from_date/to_date",
                                  max_length=128, null=True, blank=True)
    from_date = models.DateField(help_text="Date project started",
                                 null=True, blank=True)
    to_date = models.DateField(help_text="Date project ended",
                               null=True, blank=True)
    loan_or_grant = models.CharField(max_length=32, null=True, blank=True)
    features = models.TextField(max_length=2048, null=True, blank=True)
    countries = models.ManyToManyField(Country, related_name='projects')
    region = models.CharField(max_length=128, null=True, blank=True)
    locality = models.CharField(max_length=128, null=True, blank=True)
    service_on_site = models.BooleanField(default=False)
    service_off_site = models.BooleanField(default=False)
    service_remote = models.BooleanField(default=False)
    position = models.CharField(max_length=256, null=True, blank=True)
    client_end = models.CharField(max_length=128, null=True, blank=True)
    client_contract = models.CharField(max_length=128, null=True, blank=True)
    client_beneficiary = models.CharField(max_length=128, null=True, blank=True)
    contract = models.CharField(max_length=64, null=True, blank=True)
    person_months = models.CharField(max_length=64, null=True, blank=True)
    activities = models.TextField(max_length=4096, null=True, blank=True)
    references = models.TextField(max_length=512, null=True, blank=True)
    cccs_subthemes = models.ManyToManyField(CCCSSubTheme, related_name='projects')
    cccs_subsectors = models.ManyToManyField(CCCSSubSector, related_name='projects')
    ifc_subthemes = models.ManyToManyField(IFCSubTheme, related_name='projects')
    ifc_sectors = models.ManyToManyField(IFCSector, related_name='projects')

    @property
    def admin_url(self):
        """
        Return admin url to change self
        """
        url_name = 'admin:{0}_{1}_change'.format(self._meta.app_label,  self._meta.model_name)
        return reverse(url_name,  args=[self.id])
