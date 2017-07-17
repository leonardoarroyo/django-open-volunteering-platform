from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
  content = models.TextField(_('Contents'), max_length=3000)
  rating = models.FloatField(_('Rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
  user = models.ForeignKey('ovp_users.User', null=True, blank=True)
  image = models.ForeignKey('ovp_uploads.UploadedImage', blank=True, null=True, verbose_name=_('image'))
  video = models.CharField(_('Video'), max_length=150, blank=False, null=False, default='')

  # Meta
  published = models.BooleanField(_('Published'), default=False)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  testimonial_date = models.DateTimeField(_('Data do depoimento'), blank=True, null=True, default=datetime.now)

  class Meta:
    app_label = 'ovp_testimonials'
    verbose_name = _('Testimonial')
    verbose_name_plural = _('Testimonials')
