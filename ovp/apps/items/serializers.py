from ovp.apps.items.models import Item, ItemImage, ItemDocument

from ovp.apps.uploads.serializers import UploadedImageSerializer, UploadedDocumentSerializer

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers


class ItemImageSerializer(ChannelRelationshipSerializer):
  image = UploadedImageSerializer(read_only=True)
  image_id = serializers.IntegerField(required=False)
  
  class Meta:
    model = ItemImage
    fields = ['id', 'image', 'image_id', 'item']
    extra_kwargs = {'item': {'write_only': True}}


class ItemDocumentSerializer(ChannelRelationshipSerializer):
  document = UploadedDocumentSerializer(read_only=True)
  document_id = serializers.IntegerField(required=False)
  
  class Meta:
    model = ItemDocument
    fields = ['id', 'document', 'document_id', 'item', 'about']
    extra_kwargs = {'item': {'write_only': True}}


class ItemSerializer(ChannelRelationshipSerializer):
  images = ItemImageSerializer(many=True, required=False)
  documents = ItemDocumentSerializer(many=True, required=False)

  class Meta:
    model = Item
    fields = ['id', 'name', 'imageable', 'imageable_id', 'images', 'documents']

  def create(self, validated_data):
    images = validated_data.pop('images', [])
    documents = validated_data.pop('documents', [])

    item = super(ItemSerializer, self).create(validated_data)

    # Images
    for image_data in images:
      image_data['item'] = item
      image_sr = ItemImageSerializer(data=image_data, context=self.context)
      image = image_sr.create(image_data)

    # Documents
    for document_data in documents:
      document_data['item'] = item
      document_sr = ItemDocumentSerializer(data=document_data, context=self.context)
      document = document_sr.create(document_data)

    return item