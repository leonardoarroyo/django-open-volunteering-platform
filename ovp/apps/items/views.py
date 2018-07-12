import json

from ovp.apps.items.models import Item, ItemImage, ItemDocument
from ovp.apps.items.serializers import ItemSerializer, ItemImageSerializer, ItemDocumentSerializer

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response
from rest_framework import status


@ChannelViewSet
class ItemViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@ChannelViewSet
class ItemImageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  queryset = ItemImage.objects.all()
  serializer_class = ItemImageSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@ChannelViewSet
class ItemDocumentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  queryset = ItemDocument.objects.all()
  serializer_class = ItemDocumentSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
