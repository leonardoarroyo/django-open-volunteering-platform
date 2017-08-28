from ovp.apps.core import models
from ovp.apps.channels.serializers import ChannelRelationshipSerializer

class LeadSerializer(ChannelRelationshipSerializer):
  class Meta:
    fields = ['name', 'email', 'phone', 'country']
    model = models.Lead
