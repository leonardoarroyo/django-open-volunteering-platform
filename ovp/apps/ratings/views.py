from ovp.apps.core import pagination

from ovp.apps.ratings import models
from ovp.apps.ratings import serializers
from ovp.apps.ratings.permissions import UserCanRateRequest

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import decorators
from rest_framework import response

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

@ChannelViewSet
class RatingRequestResourceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  lookup_field = 'uuid'
  pagination_class = pagination.NoPagination

  @decorators.action(methods=["POST"], detail=True)
  def rate(self, request, *args, **kwargs):
    ctx = self.get_serializer_context()
    ctx['rating_request'] = self.get_object()

    # Owner
    request.data['owner'] = request.user.pk

    # Request
    request.data['request'] = ctx['rating_request'].pk

    serializer = self.get_serializer_class()(data=request.data, context=ctx)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response({"success": True}, status=200)

  def get_queryset(self, *args, **kwargs):
    return models.RatingRequest.objects.filter(requested_user = self.request.user)

  def get_serializer_class(self, *args, **kwargs):
    if self.action == 'rate':
      return serializers.RatingCreateSerializer

    return serializers.RatingRequestRetrieveSerializer

  def get_permissions(self):
    if self.action == 'list':
      self.permission_classes = (permissions.IsAuthenticated, )

    if self.action == 'retrieve':
      self.permission_classes = (permissions.IsAuthenticated, )

    if self.action == 'rate':
      self.permission_classes = (permissions.IsAuthenticated, UserCanRateRequest)

    return super(RatingRequestResourceViewSet, self).get_permissions()