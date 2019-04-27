from rest_framework import serializers
from ovp.apps.donations.validators import organization_accepts_donations

class DonateSerializer(serializers.Serializer):
  token = serializers.CharField()
  amount = serializers.IntegerField()
  organization_id = serializers.IntegerField()

  def validate(self, data):
    pre_validation = super(DonateSerializer, self).validate(data)
    organization_accepts_donations(data.get("organization_id", None))
    return pre_validation