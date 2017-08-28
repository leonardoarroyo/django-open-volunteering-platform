from rest_framework import serializers
from ovp.apps.projects import models
from ovp.apps.users import serializers as user

class CommentsRetrieveSerializer(serializers.ModelSerializer):
	user = user.UserProjectRetrieveSerializer()
	class Meta:
		model = models.Comments
		fields = ['id', 'content', 'reply_to', 'created_date', 'user']

class CommentsCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Comments
		fields = ['project', 'content', 'reply_to', 'user']

