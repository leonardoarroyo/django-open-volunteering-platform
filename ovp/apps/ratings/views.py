from rest_framework import viewsets
from rest_framework import mixins

@ChannelViewSet
class RatingResourceViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  hi
  """
  pass
