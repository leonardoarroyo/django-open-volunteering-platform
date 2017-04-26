from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonials(models.Model):
  content = models.TextField(_('Company Relationship'), max_length=3000)
  rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)])
  user = models.ForeignKey('ovp_users.User')
