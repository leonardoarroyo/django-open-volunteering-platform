from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
  content = models.TextField(_('Contents'), max_length=3000)
  rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
  user = models.ForeignKey('ovp_users.User', null=True, blank=True)

  # Meta
  published = models.BooleanField(_('Published'), default=False)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)

  class Meta:
    app_label = 'ovp_testimonials'
    verbose_name = _('Testimonial')
    verbose_name_plural = _('Testimonials')
