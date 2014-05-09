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


class IFCSector(UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Sector'
        verbose_name_plural = 'IFC Sectors'

