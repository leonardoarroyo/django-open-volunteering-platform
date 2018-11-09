import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

POSSIBLE_TYPES = (
  (1, "Qualitative"),
  (2, "Quantitative"),
  (3, "Boolean"),
)
class RatingParameter(ChannelRelationship):
  slug = models.CharField(_('Name'), max_length=100, unique=True)
  description = models.TextField(_('Description'))
  type = models.IntegerField(_('Parameter type'), choices=POSSIBLE_TYPES)

class Rating(ChannelRelationship):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  owner = models.ForeignKey('users.User', related_name='ratings_posted')
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  request = models.ForeignKey('ratings.RatingRequest')

class RatingAnswer(ChannelRelationship):
  rating = models.ForeignKey('ratings.Rating', related_name="answers")
  parameter = models.ForeignKey('ratings.RatingParameter')
  value_quantitative = models.FloatField('quantitative value', null=True)
  value_qualitative = models.TextField('qualitative value', blank=True, null=True)

class RatingRequest(ChannelRelationship):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  requested_user = models.ForeignKey('users.User', related_name='rating_requests')
  rating_parameters = models.ManyToManyField('ratings.RatingParameter')
  created_date = models.DateTimeField(auto_now_add=True)

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  rated_object = GenericForeignKey()