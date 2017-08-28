from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

class FaqCategory(ChannelRelationship):
  name = models.CharField(_('Category name'), max_length=100)

  def __str__(self):
    return self.name
