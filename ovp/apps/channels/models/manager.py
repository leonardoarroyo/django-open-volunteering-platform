from django.db import models
from ovp.apps.channels.models.mixins import ChannelCreatorMixin

class ChannelRelationshipManager(ChannelCreatorMixin, models.Manager):
  """
  All models that extend from ChannelRelationship must have ChannelRelationshipManager
  or another manager that extends from it.

  This manager overrides the .create() method so all objects created with .objects.create()
  get associated with channels.
  """
  def create(self, *args, **kwargs):
    channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    obj = super(ChannelRelationshipManager, self).create(*args, **kwargs)

    # super().create will create the object with .save() and therefore
    # with default mixins, we clear it and associate the correct channels
    # TODO: Find a better approach that cover both .save() and objects.create()
    obj.channels.clear()
    self.associate_channels(obj, channels)

    return obj
