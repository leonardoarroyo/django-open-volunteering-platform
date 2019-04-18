from django.db import models

class Subscription(models.Model):
  user = models.ForeignKey('users.user', on_delete=models.CASCADE)
  organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)