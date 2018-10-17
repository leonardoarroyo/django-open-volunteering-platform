from django.db import models
from django.utils.translation import ugettext_lazy as _

POSSIBLE_TYPES = (
  (1, "Qualitative"),
  (2, "Quantitative"),
)
class RatingParameter(models.Model):
  name = models.CharField(_('Name'), max_length=100)
  description = models.TextField(_('Description'))
  type = models.IntegerField(_('Parameter type'), choices=POSSIBLE_TYPES)

class Rating(models.Model):
  owner = models.ForeignKey('users.User')
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

class RatingAnswer(models.Model):
  rating = models.ForeignKey('ratings.Rating')
  parameter = models.ForeignKey('ratings.RatingParameter')
  value_quantitative = models.FloatField('quantitative value', null=True)
  value_qualitative = models.TextField('qualitative value', blank=True, null=True)