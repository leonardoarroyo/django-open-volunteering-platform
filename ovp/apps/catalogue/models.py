from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

class Catalogue(ChannelRelationship):
  name = models.CharField(_("Name"), max_length=100)

class Section(ChannelRelationship):
  catalogue = models.ForeignKey("catalogue.Catalogue")
  name = models.CharField(_("Name"), max_length=100)
  slug = models.CharField(_("Slug"), max_length=100)

class SectionFilter(ChannelRelationship):
  section = models.ForeignKey("catalogue.Section")
