from django.db import models
from ovp.apps.channels.models.mixins import SingleChannelCreatorMixin

class ChannelRelationshipManager(models.Manager):
  def create(self, *args, **kwargs):
    object_channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    # We don't use super().create here because the parent .create()
    # doesn't pass kwargs down to .save() method
    obj = self.model(**kwargs)
    self._for_write = True
    obj.save(force_insert=True, using=self.db, object_channels=object_channels)

    return obj

class SingleChannelRelationshipManager(SingleChannelCreatorMixin, ChannelRelationshipManager):
  """
  All models that extend from SingleChannelRelationship must use this manager
  or another manager that extends from it.

  This manager overrides the .create() method so all objects created with .objects.create()
  get associated with channels.
  """
  def create(self, *args, **kwargs):
    self.check_direct_channel_association_kwargs(kwargs)
    return super(SingleChannelRelationshipManager, self).create(*args, **kwargs)
