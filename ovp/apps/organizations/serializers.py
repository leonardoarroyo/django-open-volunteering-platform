from django.core.exceptions import ValidationError

from ovp.apps.uploads.serializers import UploadedImageSerializer

from ovp.apps.users.models.user import User

from ovp.apps.core.models import Cause
from ovp.apps.core.serializers import GoogleAddressSerializer, GoogleAddressCityStateSerializer, GoogleAddressLatLngSerializer
from ovp.apps.core.serializers.cause import CauseSerializer, CauseAssociationSerializer

from ovp.apps.organizations import models
from ovp.apps.organizations import validators
from ovp.apps.organizations.decorators import hide_address

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields
from rest_framework.compat import set_many
from rest_framework.utils import model_meta


class OrganizationCreateSerializer(ChannelRelationshipSerializer):
  address = GoogleAddressSerializer(required=False)
  causes = CauseAssociationSerializer(many=True, required=False)
  image = UploadedImageSerializer()

  class Meta:
    model = models.Organization
    fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover', 'hidden_address', 'causes', 'contact_name', 'contact_email', 'contact_phone']

  def create(self, validated_data):
    causes = validated_data.pop('causes', [])
    address_data = validated_data.pop('address', None)

    # Address
    if address_data:
      address_sr = GoogleAddressSerializer(data=address_data, context=self.context)
      address = address_sr.create(address_data)
      validated_data['address'] = address

    # Organization
    organization = super(OrganizationCreateSerializer, self).create(validated_data)

    # Associate causes
    for cause in causes:
      c = Cause.objects.get(pk=cause['id'])
      organization.causes.add(c)

    return organization

  def update(self, instance, validated_data):
    causes = validated_data.pop('causes', [])
    address_data = validated_data.pop('address', None)

    # Iterate and save fields as drf default
    info = model_meta.get_field_info(instance)
    for attr, value in validated_data.items():
      if attr in info.relations and info.relations[attr].to_many: # pragma: no cover
        set_many(instance, attr, value)
      else:
        setattr(instance, attr, value)

    # Save related resources
    if address_data:
      address_sr = GoogleAddressSerializer(data=address_data, context=self.context)
      address = address_sr.create(address_data)
      instance.address = address

    # Associate causes
    if causes:
      instance.causes.clear()
      for cause in causes:
        c = Cause.objects.get(pk=cause['id'])
        instance.causes.add(c)

    instance.save()

    return instance

class UserOrganizationRetrieveSerializer(ChannelRelationshipSerializer):
  class Meta:
    model = User
    fields = ['name', 'email', 'phone']

class OrganizationSearchSerializer(ChannelRelationshipSerializer):
  address = GoogleAddressCityStateSerializer()
  image = UploadedImageSerializer()
  is_bookmarked = serializers.BooleanField()

  class Meta:
    model = models.Organization
    fields = ['id', 'slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'is_bookmarked']

class OrganizationRetrieveSerializer(ChannelRelationshipSerializer):
  address = GoogleAddressLatLngSerializer()
  image = UploadedImageSerializer()
  cover = UploadedImageSerializer()
  causes = CauseSerializer(many=True)
  owner = UserOrganizationRetrieveSerializer()
  is_bookmarked = serializers.SerializerMethodField()

  class Meta:
    model = models.Organization
    fields = ['slug', 'owner', 'name', 'website', 'facebook_page', 'address', 'details', 'description', 'type', 'image', 'cover', 'published', 'hidden_address', 'causes', 'contact_name', 'contact_phone', 'contact_email', 'is_bookmarked']

  def get_is_bookmarked(self, instance):
    user = self.context['request'].user
    if user.is_authenticated():
      return instance.is_bookmarked(user)
    return False

  @hide_address
  def to_representation(self, instance):
    return super(OrganizationRetrieveSerializer, self).to_representation(instance)


class OrganizationInviteSerializer(serializers.Serializer):
  email = fields.EmailField(validators=[validators.invite_email_validator])

  class Meta:
    fields = ['email']

class MemberRemoveSerializer(serializers.Serializer):
  email = fields.EmailField(validators=[validators.invite_email_validator])

  class Meta:
    fields = ['email']

class OrganizationOwnerRetrieveSerializer(ChannelRelationshipSerializer):
  image = UploadedImageSerializer()
  class Meta:
    model = models.Organization
    fields = ['slug', 'name', 'description', 'image']
