from django.db import models
from django.core.urlresolvers import reverse

from mezzanine.core.models import RichText, Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED

from taggit.managers import TaggableManager


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
    plural_name = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)

    @property
    def plural(self):
        if self.plural_name is None or len(self.plural_name) == 0:
            return u"{0}s".format(self.name)
        else:
            return self.plural_name


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


class UniqueNamedWithAbbreviation(UniqueNamed):
    abbreviation = models.CharField(max_length=18, default='')

    class Meta(UniqueNamed.Meta):
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.abbreviation:
            self.abbreviation = self.abbreviation_candidate
        super(UniqueNamedWithAbbreviation, self).save(force_insert, force_update, using, update_fields)

    @property
    def abbreviation_candidate(self):
        try:
            return self.name[0:self.name.index(":")]
        except ValueError:
            return ''.join([word[0] for word in self.name.split()])


class CCCSTheme(HasProjectsMixin, UniqueNamedWithAbbreviation):

    class Meta(UniqueNamedWithAbbreviation.Meta):
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
        ordering = ['theme__name', 'name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.abbreviation, self.name)


class CCCSSector(HasProjectsMixin, UniqueNamedWithAbbreviation):

    class Meta(UniqueNamedWithAbbreviation.Meta):
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
        ordering = ['sector__name', 'name']
        unique_together = ('sector', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.sector.abbreviation, self.name)

    @property
    def projects(self):
        return Project.objects.filter(cccs_subsectors=self)


class IFCTheme(HasProjectsMixin, UniqueNamedWithAbbreviation):

    class Meta(UniqueNamedWithAbbreviation.Meta):
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
        ordering = ['theme__name', 'name']
        unique_together = ('theme', 'name')

    def __unicode__(self):
        return u"{0}/{1}".format(self.theme.abbreviation, self.name)


class IFCSector(HasProjectsMixin, UniqueNamed):

    class Meta(UniqueNamed.Meta):
        verbose_name = 'IFC Sector'
        verbose_name_plural = 'IFC Sectors'


class Project(RichText, Displayable):
    date_range = models.CharField(help_text="Deprecate and copy values into from_date/to_date",
                                  max_length=128, null=True, blank=True)
    from_date = models.DateField(help_text="Date project started",
                                 null=True, blank=True)
    to_date = models.DateField(help_text="Date project ended",
                               null=True, blank=True)
    loan_or_grant = models.CharField('Loan or Grant No.', max_length=32, null=True, blank=True)
    countries = models.ManyToManyField(Country, related_name='projects', verbose_name="Country / Countries")
    region = models.CharField(max_length=128, null=True, blank=True)
    locality = models.CharField(max_length=128, null=True, blank=True)
    cccs_subthemes = models.ManyToManyField(CCCSSubTheme, related_name='projects', null=True, blank=True,
                                            verbose_name='CCCS Sub-Theme(s)')
    cccs_subsectors = models.ManyToManyField(CCCSSubSector, related_name='projects', null=True, blank=True,
                                             verbose_name='CCCS Sub-Sector(s)')
    ifc_subthemes = models.ManyToManyField(IFCSubTheme, related_name='projects', null=True, blank=True,
                                           verbose_name='IFC Performance Standard (by Sub-Theme)')
    ifc_sectors = models.ManyToManyField(IFCSector, related_name='projects', null=True, blank=True,
                                         verbose_name='IFC Sector(s)')
    tags = TaggableManager(blank=True)
    owner = models.CharField('Project Owner/Operator', max_length=128, null=True, blank=True)
    sponsor = models.CharField('Project Financer/Sponsor', max_length=128, null=True, blank=True)

    class Meta:
        ordering = ('title',)

    @property
    def admin_url(self):
        """
        Return admin url to change self
        """
        url_name = 'admin:{0}_{1}_change'.format(self._meta.app_label,  self._meta.model_name)
        return reverse(url_name,  args=[self.id])

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project-detail", args=(self.slug,))

# Override inherited verbose names
Project._meta.get_field('short_url').verbose_name = 'Short URL'
Project._meta.get_field('_meta_title').verbose_name = 'Meta Title'


class SubProject(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('project', 'name')
        verbose_name = 'Sub-project'
        verbose_name_plural = 'Sub-projects'

    def __unicode__(self):
        return u'{0}'.format(self.name)