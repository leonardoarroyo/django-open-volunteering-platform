import uuid
from django.db import models
from ovp.apps.channels.models import ChannelRelationship

class Subscription(ChannelRelationship):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  user = models.ForeignKey('users.user', on_delete=models.CASCADE)
  organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)