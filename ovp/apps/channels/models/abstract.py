from django.db import models
from ovp.apps.channels.models.manager import ChannelRelationshipManager
from ovp.apps.channels.models.mixins import ChannelCreatorMixin

class ChannelRelationship(ChannelCreatorMixin, models.Model):
  """
  All models that are associated with channels should extend from this class
  or SingleChannelRelationship

  It has three functions:
    * Create a relationship between the object and the channels
    * Override .save() method so all new objects get associated with channels
    * Oerride the object manager so objects created with .objects.create() get
        associated with channels
  """
  channels = models.ManyToManyField('channels.Channel', related_name="%(class)s_channels")

  # Manager
  objects = ChannelRelationshipManager()

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

    super(ChannelRelationship, self).save(*args, **kwargs)

    if creating:
      self.associate_channels(self, channels)
