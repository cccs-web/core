from django.db import models
from django.core.urlresolvers import reverse


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

    @property
    def projects(self):
        return Project.objects.filter(**self.project_filter_kwargs)

    @property
    def project_filter_kwargs(self):
        raise Exception("project_filter_kwargs must be overridden in {0}".format(self.__class__))


class UniqueNamed(CCCSModel):
    name = models.CharField(max_length=512, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


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

    @property
    def project_filter_kwargs(self):
        return {'countries': self}


class CCCSTheme(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Theme'
        verbose_name_plural = 'CCCS Themes'

    @property
    def project_filter_kwargs(self):
        return {'cccs_subtheme__theme': self}


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

    @property
    def project_filter_kwargs(self):
        return {'cccs_subtheme': self}


class CCCSSector(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Sector'
        verbose_name_plural = 'CCCS Sectors'

    @property
    def project_filter_kwargs(self):
        return {'cccs_subsector__sector': self}


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

    @property
    def project_filter_kwargs(self):
        return {'cccs_subsector': self}


class IFCTheme(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Theme'
        verbose_name_plural = 'IFC Themes'

    @property
    def project_filter_kwargs(self):
        return {'ifc_subtheme__theme': self}


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

    @property
    def project_filter_kwargs(self):
        return {'ifc_subtheme': self}


class IFCSector(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Sector'
        verbose_name_plural = 'IFC Sectors'

    @property
    def project_filter_kwargs(self):
        return {'ifc_sector': self}


class Project(UniqueNamed):
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
    cccs_subtheme = models.ForeignKey(CCCSSubTheme, null=True, blank=True)
    cccs_subsector = models.ForeignKey(CCCSSubSector, null=True, blank=True)
    ifc_subtheme = models.ForeignKey(IFCSubTheme, null=True, blank=True)
    ifc_sector = models.ForeignKey(IFCSector, null=True, blank=True)

    @property
    def admin_url(self):
        """
        Return admin url to change self
        """
        url_name = 'admin:{0}_{1}_change'.format(self._meta.app_label,  self._meta.model_name)
        return reverse(url_name,  args=[self.id])
