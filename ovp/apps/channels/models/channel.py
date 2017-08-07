from django.db import models
from django.utils.translation import ugettext_lazy as _

class Channel(models.Model):
	name = models.CharField(_('Name'), max_length=100)
	slug = models.CharField(_('Slug'), max_length=100)

class ChannelCreatorMixin():
  """
  This mixin is used by ChannelRelationshipManager and ChannelRelationship.

  It contains basic functionality to associate a object with a channel.
  """
  def pop_channels_from_kwargs(self, kwargs):
    return kwargs.pop("object_channels", ["default"]), kwargs

  def associate_channels(self, instance, channel_list):
    for channel in channel_list:
      instance.channels.add(Channel.objects.get(slug=channel))

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


class ChannelRelationship(ChannelCreatorMixin, models.Model):
  """
  All models that are associated with channels should extend from this class.

  It has three functions:
    * Create a relationship between the object and the channels
    * Override .save() method so all new objects get associated with channels
    * Oerride the object manager so objects created with .objects.create() get
        associated with channels
  """
  channels = models.ManyToManyField(Channel, related_name="%(class)s_channels")

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
