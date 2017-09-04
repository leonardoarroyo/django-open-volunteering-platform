from rest_framework import serializers
from ovp.apps.core import models
from ovp.apps.users import serializers as user

class CommentaryRetrieveSerializer(serializers.ModelSerializer):
	user = user.UserProjectRetrieveSerializer()
	class Meta:
		model = models.Commentary
		fields = ['id', 'content', 'reply_to', 'created_date', 'user']

class CommentaryCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Commentary
		fields = ['content', 'reply_to', 'user']

