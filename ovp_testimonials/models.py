from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
  content = models.TextField(_('Company Relationship'), max_length=3000)
  rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)])
  user = models.ForeignKey('ovp_users.User')

  # Meta
  published = models.BooleanField(_('Published'), default=False)
  published_date = models.DateTimeField(_('Published date'), blank=True, null=True)
  deleted = models.BooleanField(_('Deleted'), default=False)
  deleted_date = models.DateTimeField(_('Deleted date'), blank=True, null=True)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True)
