from ovp.apps.faq.models.faq import Faq
from ovp.apps.faq.serializers.faq import FaqRetrieveSerializer

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response

@ChannelViewSet
class FaqResourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = Faq.objects.all()

  def list(self, request):
    """
    Retrieve list of frequently asked questions.
    """
    category = request.data.get('category', None)
    queryset = self.get_queryset()
    if category:
      queryset = queryset.filter(category=category)

    serializer = FaqRetrieveSerializer(queryset, many=True)

    return response.Response(serializer.data)

  def get_serializer_class(self):
    if self.action == 'list':
      return FaqRetrieveSerializer
