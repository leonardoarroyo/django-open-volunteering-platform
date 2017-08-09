from django.db import models
from ovp.apps.channels.models.mixins import MultiChannelCreatorMixin
from ovp.apps.channels.models.mixins import SingleChannelCreatorMixin

class MultiChannelRelationshipManager(MultiChannelCreatorMixin, models.Manager):
  """
  All models that extend from MultiChannelRelationship must have SingleChannelRelationshipManager
  or another manager that extends from it.

  This manager overrides the .create() method so all objects created with .objects.create()
  get associated with channels.
  """
  def create(self, *args, **kwargs):
    object_channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    obj = super(MultiChannelRelationshipManager, self).create(*args, **kwargs)

    # super().create will create the object with .save() and therefore
    # with default mixins, we clear it and associate the correct channels
    # TODO: Find a better approach that cover both .save() and objects.create()
    obj.channels.clear()
    self.associate_channels(obj, object_channels)

    return obj


class SingleChannelRelationshipManager(SingleChannelCreatorMixin, models.Manager):
  """
  All models that extend from ChannelRelationship must have ChannelRelationshipManager
  or another manager that extends from it.

  This manager overrides the .create() method so all objects created with .objects.create()
  get associated with a channel.
  """
  def create(self, *args, **kwargs):
    object_channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    # We don't use super().create here because the parent .create()
    # doesn't pass kwargs down to .save() method
    obj = self.model(**kwargs)
    self._for_write = True
    obj.save(force_insert=True, using=self.db, object_channels=object_channels)
    return obj
