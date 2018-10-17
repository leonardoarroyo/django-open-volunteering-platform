from django.db import models
from django.utils.translation import ugettext_lazy as _

class RatedModelMixin(models.Model):
  rating_parameters = models.ManyToManyField('ratings.RatingParameter')
  ratings = models.ManyToManyField('ratings.Rating')
  rating = models.FloatField(_('Rating'), null=True, default=None)
  
  class Meta:
    abstract = True