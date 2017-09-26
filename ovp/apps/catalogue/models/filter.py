from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

FILTER_TYPES = (
  ("CATEGORY", "Category"),
)

class Filter(ChannelRelationship):
  def __str__(self):
    return "Base filter"

  class Meta:
    abstract = True

class CategoryFilter(Filter):
  categories = models.ManyToManyField("projects.Category")

  def __str__(self):
    return "Category Filter"
