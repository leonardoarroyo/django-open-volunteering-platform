from rest_framework import serializers

from ovp.apps.gallery.models import Gallery
from ovp.apps.uploads.models import UploadedImage
from ovp.apps.channels.serializers import ChannelRelationshipSerializer
from ovp.apps.uploads.serializers import (UploadedImageSerializer,
                                          UploadedImageAssociationSerializer)


class GalleryRetrieveSerializer(ChannelRelationshipSerializer):
  images = UploadedImageSerializer(many=True)

  class Meta:
    model = Gallery
    fields = ('uuid', 'owner', 'name', 'description', 'images')
    read_only_fields = ('uuid', )
    extra_kwargs = {'owner': {'write_only': True}}


class GalleryCreateUpdateSerializer(ChannelRelationshipSerializer):
  images = UploadedImageAssociationSerializer(many=True)

  class Meta:
    model = Gallery
    fields = ('uuid', 'owner', 'name', 'description', 'images')
    read_only_fields = ('uuid', )
    extra_kwargs = {'owner': {'write_only': True}}

  def create(self, validated_data):
    images = validated_data.pop('images', [])

    gallery = super(GalleryCreateUpdateSerializer, self).create(validated_data)
    # Associate images to gallery
    for image in images:
      i = UploadedImage.objects.get(pk=image['id'])
      gallery.images.add(i)

    return gallery


class AssociateWithModel(serializers.Serializer):
  model_label = serializers.CharField()
  pk = serializers.CharField()

  class Meta:
    fields = ('model_label', 'pk')
