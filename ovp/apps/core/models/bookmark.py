from django.db import models
from ovp.apps.channels.models.abstract import ChannelRelationship

class AbstractBookmark(ChannelRelationship):
  user = models.ForeignKey('users.User')

  class Meta:
    abstract = True
