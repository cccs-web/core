from django.db import models


class UniqueNamed(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


class Country(UniqueNamed):
    """
    There are lots of unique indexes here; the table is often used and rarely updated.
    """
    iso_english_name = models.CharField(max_length=80, unique=True)
    fips = models.CharField(max_length=2, null=True, blank=True)
    iso_numeric = models.IntegerField(null=True, blank=True)
    iso_3166 = models.CharField(max_length=3, null=True, blank=True)
    iso = models.CharField(max_length=7, null=True, blank=True)
    notes = models.TextField(max_length=512, null=True, blank=True)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.iso)


class CCCSTheme(UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Theme'
        verbose_name_plural = 'CCCS Themes'


class CCCSSubTheme(models.Model):
    name = models.CharField(max_length=128)
    theme = models.ForeignKey(CCCSTheme, related_name='sub_themes')

    class Meta:
        verbose_name = 'CCCS SubTheme'
        verbose_name_plural = 'CCCS SubThemes'
        ordering = ['name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.name, self.name)


class CCCSSector(UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'CCCS Sector'
        verbose_name_plural = 'CCCS Sectors'


class CCCSSubSector(models.Model):
    name = models.CharField(max_length=128)
    sector = models.ForeignKey(CCCSSector, related_name='sub_themes')

    class Meta:
        verbose_name = 'CCCS SubSector'
        verbose_name_plural = 'CCCS SubSectors'
        ordering = ['name']
        unique_together = ('sector', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.sector.name, self.name)


class IFCTheme(UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Theme'
        verbose_name_plural = 'IFC Themes'


class IFCSubTheme(models.Model):
    name = models.CharField(max_length=128)
    theme = models.ForeignKey(IFCTheme, related_name='sub_themes')

    class Meta:
        verbose_name = 'IFC SubTheme'
        verbose_name_plural = 'IFC SubThemes'
        ordering = ['name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.name, self.name)


class IFCSector(UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Sector'
        verbose_name_plural = 'IFC Sectors'


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
