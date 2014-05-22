from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from projects.models import Country

from mezzanine.utils.urls import unique_slug, slugify


class CV(models.Model):
    user = models.OneToOneField(User, related_name="cv")
    slug = models.CharField(max_length=512, null=True, blank=True, unique=True)
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
        return reverse("cv-detail", args=(self.id,))

    def save(self, *args, **kwargs):
        """
        If no slug is provided, generates one before saving.
        """
        if not self.slug and self.user.first_name:
            self.slug = self.generate_unique_slug()
        super(CV, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to
        utils.urls.unique_slug, which appends an index if necessary.
        """
        slug_qs = type(self).objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())

    def get_slug(self):
        return slugify(u"{0}-{1}-{2}".format(self.user.first_name,
                                             self.middle_names,
                                             self.user.last_name))