from rest_framework import serializers
from rest_framework import fields

class ContactFormSeralizer(serializers.Serializer):
  name = fields.CharField()
  message = fields.CharField()
  email = fields.CharField()
  phone = fields.CharField()
  recipients = fields.ListField()

  class Meta:
    fields = ['name', 'message', 'email', 'phone']