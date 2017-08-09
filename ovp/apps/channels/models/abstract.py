from django.db import models

from ovp.apps.channels.models.channel import Channel

from ovp.apps.channels.models.manager import MultiChannelRelationshipManager
from ovp.apps.channels.models.manager import SingleChannelRelationshipManager

from ovp.apps.channels.models.mixins import MultiChannelCreatorMixin
from ovp.apps.channels.models.mixins import SingleChannelCreatorMixin

from ovp.apps.channels.exceptions import UnexpectedChannelAssociationError

class MultiChannelRelationship(MultiChannelCreatorMixin, models.Model):
  """
  All models that are associated with channels should extend from this class
  or SingleChannelRelationship

  It has three functions:
    * Create a relationship between the object and the channels
    * Override .save() method so all new objects get associated with channels
    * Oerride the object manager so objects created with .objects.create() get
        associated with channels
  """
  channels = models.ManyToManyField(Channel, related_name="%(class)s_channels")

  # Manager
  objects = MultiChannelRelationshipManager()

  class Meta:
    abstract = True

  def save(self, *args, **kwargs):
    """
    We override save method to associate the requested channels with the
    saved object.
    """
    creating = False
    if not self.pk:
      creating = True

    channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    super(MultiChannelRelationship, self).save(*args, **kwargs)

    if creating:
      self.associate_channels(self, channels)


class SingleChannelRelationship(SingleChannelCreatorMixin, models.Model):
  """
  All models that are associated with a single channel should extend from this class.

  It has three functions:
    * Create a relationship between the object and a single channel
    * Override .save() method so all new objects get associated with a channel
    * Oerride the object manager so objects created with .objects.create() get
        associated with a single channel
  """
  channel = models.ForeignKey(Channel, related_name="%(class)s_channel")

  # Manager
  objects = SingleChannelRelationshipManager()

  class Meta:
    abstract = True

  def save(self, *args, **kwargs):
    """
    We override save method to associate the requested channels with the
    saved object.
    """
    if not self.pk:
      try:
        self.channel
        raise UnexpectedChannelAssociationError()
      except Channel.DoesNotExist:
        channel, kwargs = self.pop_channel_as_object_from_kwargs(kwargs)
        self.associate_channel(self, channel)

    super(SingleChannelRelationship, self).save(*args, **kwargs)
