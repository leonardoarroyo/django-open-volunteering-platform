from ovp.apps.channels.serializers import ChannelRelationshipSerializer
from ovp.apps.projects.models import VolunteerRole

from rest_framework import serializers

class VolunteerRoleSerializer(ChannelRelationshipSerializer):
  id = serializers.ModelField(model_field=VolunteerRole()._meta.get_field("id"))
  class Meta:
    model = VolunteerRole
    fields = ['name', 'prerequisites', 'details', 'vacancies', 'applied_count', 'id']

class VolunteerRoleApplySerializer(ChannelRelationshipSerializer):
  class Meta:
    model = VolunteerRole
    fields = ['name', 'details', 'id']
