from rest_framework import serializers
from ovp.apps.projects import models
from ovp.apps.users import serializers

class CommentsRetrieveSerializer(serializers.ModelSerializer):
	user = serializers.UserRetrieveSerializer()
  class Meta:
    model = models.Comments
    fields = ['id', 'name', 'content', 'reply_to', 'created_date', 'user']

class CommentsCreateSerializer(serializers.ModelSerializer):
	class Meta:
    model = models.Comments
    fields = ['name', 'content', 'reply_to', 'user']

