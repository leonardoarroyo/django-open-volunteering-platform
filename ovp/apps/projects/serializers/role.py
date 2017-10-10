from ovp.apps.channels.serializers import ChannelRelationshipSerializer
from ovp.apps.projects.models import VolunteerRole

class VolunteerRoleSerializer(ChannelRelationshipSerializer):
  class Meta:
    model = VolunteerRole
    fields = ['name', 'prerequisites', 'details', 'vacancies', 'applied_count', 'id']

class VolunteerRoleApplySerializer(ChannelRelationshipSerializer):
  class Meta:
    model = VolunteerRole
    fields = ['name', 'details', 'id']
