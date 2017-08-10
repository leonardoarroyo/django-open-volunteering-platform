from rest_framework import mixins

class CreateModelWithChannelMixin(mixins.CreateModelMixin):
  """
  A viewset mixin to be used instead of CreateModelMixin if the
  viewset model extends ChannelRelationship abstract model
  """
  def perform_create(self, serializer):
    channels = self.request.channels
    serializer.save(object_channels=channels)
