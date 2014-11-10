from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import signals
from mezzanine.core.models import RichText, Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from django.core.exceptions import ValidationError
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


def project_pre_save(sender, instance, **kwargs):
    _path = instance.title
    if instance.parent:
        _path = instance.parent.title + ' / ' +  _path

    instance.path = _path

def project_post_save(sender, instance, **kwargs):

    if instance.parent:
        min_from_date, max_to_date = instance.parent.get_date_range()

        #pevent sending a signal
        Project.objects.filter(id=instance.parent.id).update(from_date=min_from_date, to_date=max_to_date)

def project_cccs_subthemes_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and instance.parent:
        for c in instance.cccs_subthemes.all():
            instance.parent.cccs_subthemes.add(c)

def project_cccs_subsectors_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and instance.parent:
        for c in instance.cccs_subsectors.all():
            instance.parent.cccs_subsectors.add(c)

def project_ifc_subthemes_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and instance.parent:
        for c in instance.ifc_subthemes.all():
            instance.parent.ifc_subthemes.add(c)

def project_ifc_sectors_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and instance.parent:
        for c in instance.ifc_sectors.all():
            instance.parent.ifc_sectors.add(c)

class Project(RichText, Displayable):
    parent = models.ForeignKey("self", verbose_name='Parent Project', null=True, blank=True)
    path = models.CharField(max_length=512, null=True, blank=True)
    date_range = models.CharField(help_text="Deprecate and copy values into from_date/to_date",
                                  max_length=128, null=True, blank=True)
    from_date = models.DateField(help_text="Date project started",
                                 null=True, blank=True)
    to_date = models.DateField(help_text="Date project ended",
                               null=True, blank=True)
    loan_or_grant = models.CharField('Loan or Grant No.', max_length=32, null=True, blank=True)
    #features = models.TextField(max_length=2048, null=True, blank=True)
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

    def clean(self):
        _errors = {}

        min_from_date, max_to_date = self.get_cv_date_range()
        if self.from_date and min_from_date and self.from_date > min_from_date:
            _errors['from_date'] = ["Project start date couldn't be set after assigned cv projects' start date.",]
        if self.to_date and max_to_date and self.to_date < max_to_date:
            _errors['to_date'] = ["Project end date couldn't be set before assigned projects' end date.",]

        if not self.parent:
            min_from_date, max_to_date = self.get_date_range()
            if self.from_date and min_from_date and self.from_date > min_from_date:
                _errors['from_date'] = ["Super project start date couldn't be set after sub projects' start date.",]
            if self.to_date and max_to_date and self.to_date < max_to_date:
                _errors['to_date'] = ["Super project end date couldn't be set before sub projects' end date.",]

            cccs_subthemes_pks_set = set(self.cccs_subthemes_pks)
            sub_cccs_subthemes_pks_set = []
            for sub in self.sub_projects:
                sub_cccs_subthemes_pks_set.extend(sub.cccs_subthemes_pks)
            sub_cccs_subthemes_pks_set = set(sub_cccs_subthemes_pks_set)
            diff_set = sub_cccs_subthemes_pks_set - cccs_subthemes_pks_set
            if len(diff_set) > 0:
                _errors['cccs_subthemes'] = ["Super project should contain all sub projects' cccs subtheme.",]

            cccs_subsectors_pks_set = set(self.cccs_subsectors_pks)
            sub_cccs_subsectors_pks_set = []
            for sub in self.sub_projects:
                sub_cccs_subsectors_pks_set.extend(sub.cccs_subsectors_pks)
            sub_cccs_subsectors_pks_set = set(sub_cccs_subsectors_pks_set)
            diff_set = sub_cccs_subsectors_pks_set - cccs_subsectors_pks_set
            if len(diff_set) > 0:
                _errors['cccs_subsectors'] = ["Super project should contain all sub projects' cccs subsectors.",]

            ifc_subthemes_pks_set = set(self.ifc_subthemes_pks)
            sub_ifc_subthemes_pks_set = []
            for sub in self.sub_projects:
                sub_ifc_subthemes_pks_set.extend(sub.ifc_subthemes_pks)
            sub_ifc_subthemes_pks_set = set(sub_ifc_subthemes_pks_set)
            diff_set = sub_ifc_subthemes_pks_set - ifc_subthemes_pks_set
            if len(diff_set) > 0:
                _errors['ifc_subthemes'] = ["Super project should contain all sub projects' ifc subthemes.",]

            ifc_sectors_pks_set = set(self.ifc_sectors_pks)
            sub_ifc_sectors_pks_set = []
            for sub in self.sub_projects:
                sub_ifc_sectors_pks_set.extend(sub.ifc_sectors_pks)
            sub_ifc_sectors_pks_set = set(sub_ifc_sectors_pks_set)
            diff_set = sub_ifc_sectors_pks_set - ifc_sectors_pks_set
            if len(diff_set) > 0:
                _errors['ifc_sectors'] = ["Super project should contain all sub projects' ifc sectors.",]


        if self.parent and len(self.sub_projects) > 0:
            _errors['parent'] = ["This project can't be sub projects because it has already child projects.",]

        if self.parent and self == self.parent:
            _errors['parent'] = ["Self can't be set as super project.", ]

        if _errors:
            raise ValidationError(_errors)

    def get_date_range(self):
        if self.parent:
            return self.from_date, self.to_date

        sub_projects = Project.objects.all().filter(parent=self)
        min_from_date = self.from_date
        max_to_date = self.to_date
        for sub_project in sub_projects:
            if not min_from_date and sub_project.from_date:
                min_from_date = sub_project.from_date
            if not max_to_date and sub_project.to_date:
                max_to_date = sub_project.to_date
            if sub_project.from_date and min_from_date > sub_project.from_date:
                min_from_date = sub_project.from_date
            if sub_project.to_date and max_to_date < sub_project.to_date:
                max_to_date = sub_project.to_date

        return min_from_date, max_to_date

    def get_cv_date_range(self):
        min_from_date = self.from_date
        max_to_date = self.to_date
        from cvs.models import CVProject
        cv_projects = CVProject.objects.filter(project=self).all()
        for sub_project in cv_projects:
            if not min_from_date and sub_project.from_date:
                min_from_date = sub_project.from_date
            if not max_to_date and sub_project.to_date:
                max_to_date = sub_project.to_date
            if sub_project.from_date and min_from_date > sub_project.from_date:
                min_from_date = sub_project.from_date
            if sub_project.to_date and max_to_date < sub_project.to_date:
                max_to_date = sub_project.to_date

        return min_from_date, max_to_date



    class Meta:
        ordering = ('path',)

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

    @property
    def sub_projects(self):
        return Project.objects.all().filter(parent=self)

    @property
    def cccs_subthemes_pks(self):
        return [c.pk for c in self.cccs_subthemes.all()]

    @property
    def cccs_subsectors_pks(self):
        return [c.pk for c in self.cccs_subsectors.all()]

    @property
    def ifc_subthemes_pks(self):
        return [c.pk for c in self.ifc_subthemes.all()]

    @property
    def ifc_sectors_pks(self):
        return [c.pk for c in self.ifc_sectors.all()]

    def get_absolute_url_pks(self):
        return reverse("project-detail", args=(self.slug,))

# Override inherited verbose names
Project._meta.get_field('short_url').verbose_name = 'Short URL'


signals.pre_save.connect(project_pre_save, sender=Project)
signals.post_save.connect(project_post_save, sender=Project)

signals.m2m_changed.connect(project_cccs_subthemes_changed, sender=Project.cccs_subthemes.through)
signals.m2m_changed.connect(project_cccs_subsectors_changed, sender=Project.cccs_subsectors.through)
signals.m2m_changed.connect(project_ifc_subthemes_changed, sender=Project.ifc_subthemes.through)
signals.m2m_changed.connect(project_ifc_sectors_changed, sender=Project.ifc_sectors.through)