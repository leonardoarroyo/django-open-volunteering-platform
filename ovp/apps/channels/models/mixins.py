from ovp.apps.channels.models import Channel

from ovp.apps.channels.exceptions import UnexpectedChannelAssociationError
from ovp.apps.channels.exceptions import UnexpectedMultipleChannelsError
from ovp.apps.channels.exceptions import NoChannelSupplied

class BaseChannelCreatorMixin():
  def pop_channels_from_kwargs(self, kwargs):
    """ Pop object_channels from kwargs, either from .save() or .manager.create() """
    channels = kwargs.pop("object_channels", None)

    if not channels:
      raise NoChannelSupplied()

    return channels, kwargs


class ChannelCreatorMixin(BaseChannelCreatorMixin):
  """
  This mixin is used by ChannelRelationshipManager and ChannelRelationship.

  It contains basic functionality to associate a object with a single channel.
  """
  def pop_channel_as_object_from_kwargs(self, kwargs):
    channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    if len(channels) > 1:
      raise UnexpectedMultipleChannelsError

    channel = Channel.objects.get(slug=channels[0])

    return channel, kwargs

  def check_direct_channel_association_instance(self):
    """
    Check if it's not trying to directly associate a channel with the model
    with obj.channel = channel, obj.save().

    Use object_channels=[channel_slug] instead.
    """
    try:
      self.channel
      raise UnexpectedChannelAssociationError()
    except Channel.DoesNotExist:
      pass

    return True

  def check_direct_channel_association_kwargs(self, kwargs):
    """
    Check if it's not trying to directly associate a channel with the manager
    create method: .manager.create(channel=channel).

    Use object_channels=[channel_slug] instead.
    """
    if "channel" in kwargs:
      raise UnexpectedChannelAssociationError()

    return True
