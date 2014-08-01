from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from projects.models import Country, UniqueNamed

from mezzanine.core.models import Displayable


class Language(UniqueNamed):
    pass


class AssociateRole(UniqueNamed):
    pass


class CV(Displayable):
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
    associate_role = models.ForeignKey(AssociateRole, null=True, blank=True)

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
                                     self.middle_names,
                                     self.user.last_name) if n])


class CVSet(models.Model):
    cv = models.ForeignKey(CV)

    class Meta:
        abstract = True


class CVDateRangeSet(CVSet):
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class CVProject(CVSet):
    project = models.ForeignKey('projects.Project')
    position = models.CharField(max_length=256, null=True, blank=True)
    person_months = models.CharField(max_length=64, null=True, blank=True)
    activities = models.TextField(max_length=4096, null=True, blank=True)
    references = models.TextField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = "CV Project"
        verbose_name_plural = "CV Projects"
        unique_together = ('cv', 'project')


class CVLearning(CVDateRangeSet):
    institution = models.CharField(max_length=128, null=True, blank=True)
    subject = models.CharField(max_length=256)

    class Meta(CVSet.Meta):
        abstract = True


class CVTraining(CVLearning):

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Training"


class CVEducation(CVLearning):
    qualification = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"


class CVMembership(CVDateRangeSet):
    organization = models.CharField(max_length=128)
    role = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"


LANGUAGE_ABILITY_CHOICES = ((5, "Native (equiv)"),
                            (4, "Fluent"),
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
    accomplishments = models.TextField(max_length=8192, null=True, blank=True)
    references = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Employment"
        verbose_name_plural = "Employment"


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