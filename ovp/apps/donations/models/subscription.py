import uuid
from django.db import models

class Subscription(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  user = models.ForeignKey('users.user', on_delete=models.CASCADE)
  organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)