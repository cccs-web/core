from calendar import monthrange
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from projects.models import Country, UniqueNamed

from mezzanine.core.models import Displayable, RichText, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from mezzanine.core.fields import RichTextField


class Language(UniqueNamed):
    pass


class CCCSRole(UniqueNamed):
    class Meta:
        verbose_name = 'CCCS Role'
        verbose_name_plural = 'CCCS Roles'


class CV(RichText, Displayable):
    user = models.OneToOneField(User, related_name="cv")
    middle_names = models.CharField(max_length=128, null=True, blank=True)
    alternate_names = models.CharField(max_length=128, null=True, blank=True)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zip = models.CharField(max_length=32, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    telephone = models.CharField(max_length=64, null=True, blank=True)
    citizenship = models.ForeignKey(Country, related_name='citizenship_set', null=True, blank=True)
    birth_country = models.ForeignKey(Country, related_name='birth_country_set', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), null=True, blank=True)
    marital_status = models.CharField(max_length=1, choices=(('M', 'Married'),
                                                             ('S', 'Single'),
                                                             ('D', 'Divorced'),
                                                             ('W', 'Widowed')), null=True, blank=True)
    cccs_role = models.ForeignKey(CCCSRole, verbose_name='CCCS Role', null=True, blank=True)

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ['user__last_name']

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def admin_url(self):
        """
        Return admin url to change self
        """
        url_name = 'admin:{0}_{1}_change'.format(self._meta.app_label,  self._meta.model_name)
        return reverse(url_name,  args=[self.id])

    def get_absolute_url(self):
        return reverse("cv-detail", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.title = self._build_title()
        super(CV, self).save(*args, **kwargs)

    def _build_title(self):
        return '-'.join([n for n in (self.user.first_name,
                                     self.user.last_name) if n])

# Override inherited verbose names (this is not good but it is what is wanted)
CV._meta.get_field('content').verbose_name = 'Biographical Profile'
CV._meta.get_field('description').verbose_name = 'HTML Page Description'
CV._meta.get_field('short_url').verbose_name = 'Short URL'


class CVSet(models.Model):
    cv = models.ForeignKey(CV)

    class Meta:
        abstract = True


class CVDateRangeSet(CVSet):
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def months(self):
        """
        Return the integer number of months (rounded up) in the date range
        """
        if self.from_date is None:
            return 0

        delta = 0
        to_date = datetime.now().date() if self.to_date is None else self.to_date

        # Go through the months to allow for num days in each month
        while True:
            mdays = monthrange(self.from_date.year, self.from_date.month)[1]
            self.from_date += timedelta(days=mdays)
            if self.from_date <= to_date:
                delta += 1
            else:
                break
        return delta


class CVProject(CVSet):
    project = models.ForeignKey('projects.Project')
    subproject = models.ForeignKey('projects.SubProject', verbose_name='Sub-Project / Tranche', null=True, blank=True)
    position = models.CharField(max_length=256, null=True, blank=True)
    person_months = models.CharField(max_length=64, null=True, blank=True)
    activities = RichTextField(null=True, blank=True)
    references = RichTextField(null=True, blank=True)
    from_date = models.DateField(help_text="Date started working on project",
                                 null=True, blank=True)
    to_date = models.DateField(help_text="Date finished working on project",
                               null=True, blank=True)
    service_on_site = models.BooleanField(default=False)
    service_off_site = models.BooleanField(default=False)
    service_remote = models.BooleanField(default=False)
    client_end = models.CharField('Sponsor / End Client', max_length=128, null=True, blank=True)
    client_contract = models.CharField('Contracted Through / Direct Client', max_length=128, null=True, blank=True)
    client_beneficiary = models.CharField('Beneficiary Client', max_length=128, null=True, blank=True)
    contract = models.CharField('Contract No.', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        unique_together = ('cv', 'project')
        ordering = ('-to_date',)

    def __unicode__(self):
        return u'{0}: {1}'.format(self.project.name, self.position)


class CVLearning(CVDateRangeSet):
    institution = models.CharField(max_length=128, null=True, blank=True)
    subject = models.CharField(max_length=256)

    class Meta(CVSet.Meta):
        abstract = True


class CVTraining(CVLearning):

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Training"
        ordering = ['-from_date']


class CVEducation(CVLearning):
    qualification = models.CharField(max_length=64, null=True, blank=True)
    minors = models.CharField('Minor(s)', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-from_date']

CVEducation._meta.get_field('subject').verbose_name = 'Major(s)/Primary Discipline(s)'


class CVMembership(CVDateRangeSet):
    organization = models.CharField(max_length=128)
    role = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Professional Membership(s)"
        verbose_name_plural = "Professional Memberships"
        ordering = ['-from_date']


LANGUAGE_ABILITY_CHOICES = ((5, "Native (equiv)"),
                            (4, "Professional"),
                            (3, "Working"),
                            (2, "Limited"),
                            (1, "Elementary"))


class CVLanguage(CVSet):
    language = models.ForeignKey(Language)
    reading = models.PositiveSmallIntegerField(choices=LANGUAGE_ABILITY_CHOICES, null=True, blank=True)
    speaking = models.PositiveSmallIntegerField(choices=LANGUAGE_ABILITY_CHOICES, null=True, blank=True)
    writing = models.PositiveSmallIntegerField(choices=LANGUAGE_ABILITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


class CVEmployment(CVDateRangeSet):
    employer = models.CharField(max_length=256)
    location = models.CharField(max_length=256, null=True, blank=True)
    position = models.CharField(max_length=256, null=True, blank=True)
    accomplishments = RichTextField(null=True, blank=True)
    references = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Employment"
        verbose_name_plural = "Employment"
        ordering = ['-from_date']

    def __unicode__(self):
        return u'{0}: {1}'.format(self.employer, self.position)


class CVPublication(CVSet):
    publication_date = models.DateField(null=True, blank=True)
    publication_type = models.CharField(max_length=256, null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=512)
    distribution = models.CharField(max_length=512, null=True, blank=True)
    identifier = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-publication_date', 'title']
