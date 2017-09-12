from rest_framework import serializers
from ovp.apps.core import models
from ovp.apps.core import validators
from ovp.apps.uploads.serializers import UploadedImageSerializer
from ovp.apps.channels.serializers import ChannelRelationshipSerializer

class FullCauseSerializer(ChannelRelationshipSerializer):
  image = UploadedImageSerializer()
  class Meta:
    fields = ['id', 'name', 'image']
    model = models.Cause

class CauseSerializer(ChannelRelationshipSerializer):
	class Meta:
		fields = ['id', 'name']
		model = models.Cause

class CauseAssociationSerializer(ChannelRelationshipSerializer):
  id = serializers.IntegerField()
  name = serializers.CharField(read_only=True)

  class Meta:
    fields = ['id', 'name']
    model = models.Cause
    validators = [validators.cause_exist]
