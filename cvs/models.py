from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from projects.models import Country

from mezzanine.core.models import Displayable


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

    def get_absolute_url(self):
        return reverse("cv-detail", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.title = self._build_title()
        super(CV, self).save(*args, **kwargs)

    def _build_title(self):
        return '-'.join([n for n in (self.user.first_name,
                                     self.middle_names,
                                     self.user.last_name) if n])


class CVProject(models.Model):
    cv = models.ForeignKey(CV)
    project = models.ForeignKey('projects.Project')
    position = models.CharField(max_length=256, null=True, blank=True)
    person_months = models.CharField(max_length=64, null=True, blank=True)
    activities = models.TextField(max_length=4096, null=True, blank=True)
    references = models.TextField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ('cv', 'project')