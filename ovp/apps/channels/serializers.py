from rest_framework import serializers

class ChannelRelationshipSerializer(serializers.ModelSerializer):
  """
  This serializer is required for models that extend ChannelRelationship.
  It automatically passes request channels down to the model.
  """
  def create(self, validated_data):
    request = self.context["request"] # Force exception if request is unavailable
    validated_data["object_channels"] = request.channels
    return super(ChannelRelationshipSerializer, self).create(validated_data)
