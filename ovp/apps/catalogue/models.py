from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

FILTER_TYPES = (
  ("CATEGORY", "Category"),
)

class Catalogue(ChannelRelationship):
  name = models.CharField(_("Name"), max_length=100)
  slug = models.SlugField(_("Slug"), max_length=100)

  def __str__(self):
    return self.name

class Section(ChannelRelationship):
  catalogue = models.ForeignKey("catalogue.Catalogue")
  name = models.CharField(_("Name"), max_length=100)
  slug = models.SlugField(_("Slug"), max_length=100)

  def __str__(self):
    return self.name

class SectionFilter(ChannelRelationship):
  section = models.ForeignKey("catalogue.Section")
  type = models.CharField(_("Filter type"), max_length=30, choices=FILTER_TYPES)
