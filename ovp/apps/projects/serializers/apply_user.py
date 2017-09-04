from ovp.apps.projects import models
from rest_framework import serializers

from ovp.apps.channels.serializers import ChannelRelationshipSerializer
from ovp.apps.core.serializers import GoogleAddressLatLngSerializer
from ovp.apps.uploads.serializers import UploadedImageSerializer
from ovp.apps.organizations.serializers import OrganizationSearchSerializer


class ProjectApplyRetrieveSerializer(ChannelRelationshipSerializer):
  image = UploadedImageSerializer()
  address = GoogleAddressLatLngSerializer()
  organization = OrganizationSearchSerializer()

  class Meta:
    model = models.Project
    fields = ['slug', 'image', 'name', 'description', 'highlighted', 'published_date', 'address', 'details', 'created_date', 'organization', 'minimum_age', 'applied_count', 'max_applies', 'max_applies_from_roles', 'closed', 'closed_date', 'published', 'hidden_address', 'crowdfunding', 'public_project']

  def to_representation(self, instance):
    return super(ProjectApplyRetrieveSerializer, self).to_representation(instance)

class ApplyUserRetrieveSerializer(ChannelRelationshipSerializer):
	project = ProjectApplyRetrieveSerializer()

	class Meta:
		model = models.Apply
		fields = ['id', 'email', 'username', 'phone', 'date', 'canceled', 'canceled_date', 'project']
