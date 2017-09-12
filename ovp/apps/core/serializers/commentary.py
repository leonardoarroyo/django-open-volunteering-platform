from rest_framework import serializers
from ovp.apps.core import models
from ovp.apps.users import serializers as user
from ovp.apps.channels.serializers import ChannelRelationshipSerializer

class CommentaryRetrieveSerializer(ChannelRelationshipSerializer):
	user = user.UserProjectRetrieveSerializer()
	class Meta:
		model = models.Commentary
		fields = ['id', 'content', 'reply_to', 'created_date', 'user']

class CommentaryCreateSerializer(ChannelRelationshipSerializer):
	class Meta:
		model = models.Commentary
		fields = ['content', 'reply_to', 'user']

