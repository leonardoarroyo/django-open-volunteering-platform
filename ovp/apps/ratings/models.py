from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
import uuid

POSSIBLE_TYPES = (
  (1, "Qualitative"),
  (2, "Quantitative"),
)
class RatingParameter(models.Model):
  name = models.CharField(_('Name'), max_length=100)
  description = models.TextField(_('Description'))
  type = models.IntegerField(_('Parameter type'), choices=POSSIBLE_TYPES)

class Rating(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  owner = models.ForeignKey('users.User', related_name='ratings_posted')
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  request = models.ForeignKey('ratings.RatingRequest')

class RatingAnswer(models.Model):
  rating = models.ForeignKey('ratings.Rating')
  parameter = models.ForeignKey('ratings.RatingParameter')
  value_quantitative = models.FloatField('quantitative value', null=True)
  value_qualitative = models.TextField('qualitative value', blank=True, null=True)

class RatingRequest(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  requested_user = models.ForeignKey('users.User', related_name='rating_requests')
  rating_parameters = models.ManyToManyField('ratings.RatingParameter')

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  rated_object = GenericForeignKey()