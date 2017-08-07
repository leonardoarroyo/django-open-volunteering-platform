from rest_framework import mixins

class CreateModelWithChannelMixin(mixins.CreateModelMixin):
  def perform_create(self, serializer):
    channels = self.request.channels
    serializer.save(object_channels=channels)
