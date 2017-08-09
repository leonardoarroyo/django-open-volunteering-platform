from ovp.apps.channels.models import Channel

from ovp.apps.channels.exceptions import UnexpectedMultipleChannelsError

class BaseChannelCreatorMixin():
  def pop_channels_from_kwargs(self, kwargs):
    return kwargs.pop("object_channels", ["default"]), kwargs


class MultiChannelCreatorMixin(BaseChannelCreatorMixin):
  """
  This mixin is used by MultiChannelRelationshipManager and MultiChannelRelationship.

  It contains basic functionality to associate a object with multiple channels.
  """
  def associate_channels(self, instance, channel_list):
    for channel in channel_list:
      instance.channels.add(Channel.objects.get(slug=channel))


class SingleChannelCreatorMixin(BaseChannelCreatorMixin):
  """
  This mixin is used by SingleChannelRelationshipManager and SingleChannelRelationship.

  It contains basic functionality to associate a object with a single channel.
  """
  def pop_channel_as_object_from_kwargs(self, kwargs):
    channels, kwargs = self.pop_channels_from_kwargs(kwargs)

    if len(channels) > 1:
      raise UnexpectedMultipleChannelsError

    channel = Channel.objects.get(slug=channels[0])

    return channel, kwargs

  def associate_channel(self, instance, channel):
    instance.channel = channel
