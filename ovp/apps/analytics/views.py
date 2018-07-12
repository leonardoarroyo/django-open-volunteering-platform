from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response

@ChannelViewSet
class AnalyticsResourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  AnalyticsResourceViewSet resource endpoint
  """
  def list(self, request):
    return response.Response({ abacate: 'hello' })

  def get_serializer_class(self):
    print(self.action)
