from django.db import models

from ovp.apps.channels.models.channel import Channel
from ovp.apps.channels.models.manager import SingleChannelRelationshipManager
from ovp.apps.channels.models.mixins import SingleChannelCreatorMixin

from ovp.apps.channels.exceptions import UnexpectedChannelAssociationError


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
      self.check_direct_channel_association_instance()
      channel, kwargs = self.pop_channel_as_object_from_kwargs(kwargs)
      self.channel = channel

    super(SingleChannelRelationship, self).save(*args, **kwargs)
