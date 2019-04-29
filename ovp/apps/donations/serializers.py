from rest_framework import serializers
from ovp.apps.donations.validators import organization_accepts_donations
from ovp.apps.donations.models import Transaction
from ovp.apps.organizations.serializers import OrganizationRetrieveSerializer

class DonateSerializer(serializers.Serializer):
  token = serializers.CharField(required=True)
  amount = serializers.IntegerField(required=True)
  organization_id = serializers.IntegerField(required=True)

  def validate(self, data):
    pre_validation = super(DonateSerializer, self).validate(data)
    organization_accepts_donations(data.get("organization_id", None))
    return pre_validation

class TransactionRetrieveSerializer(serializers.ModelSerializer):
  organization = OrganizationRetrieveSerializer()
  
  class Meta:
    fields = ["uuid", "organization", "amount", "status", "date_created", "date_modified"]
    model = Transaction

class RefundTransactionSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(required=True)