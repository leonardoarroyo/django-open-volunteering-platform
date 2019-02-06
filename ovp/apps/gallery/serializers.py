from ovp.apps.gallery.models import Gallery

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers

class GallerySerializer(ChannelRelationshipSerializer):
  class Meta:
    model = Gallery
    fields = ('uuid', 'owner', 'name', 'description')
    read_only_fields = ('uuid', )
    extra_kwargs = {'owner': {'write_only': True}}

class AssociateWithModel(serializers.Serializer):
  model_label = serializers.CharField()
  pk = serializers.CharField()

  class Meta:
    fields = ('model_label', 'pk')