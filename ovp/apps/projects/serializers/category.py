from ovp.apps.channels.serializers import ChannelRelationshipSerializer
from ovp.apps.projects import models
from rest_framework import serializers

class CategoryRetrieveSerializer(ChannelRelationshipSerializer):
  class Meta:
    model = models.Category
    fields = ['id', 'name', 'description', 'image', 'highlighted', 'slug']
