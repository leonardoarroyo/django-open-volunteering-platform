from ovp.apps.channels.models import Channel

class MultiChannelCreatorMixin():
  """
  This mixin is used by ChannelRelationshipManager and ChannelRelationship.

  It contains basic functionality to associate a object with a channel.
  """
  def pop_channels_from_kwargs(self, kwargs):
    return kwargs.pop("object_channels", ["default"]), kwargs

  def associate_channels(self, instance, channel_list):
    for channel in channel_list:
      instance.channels.add(Channel.objects.get(slug=channel))
