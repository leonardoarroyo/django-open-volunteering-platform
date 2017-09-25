
from django.db import models

from ovp.apps.channels.models.abstract import ChannelRelationship

from django.utils.translation import ugettext_lazy as _

class OrganizationInvite(ChannelRelationship):
  organization = models.ForeignKey("organizations.Organization")
  invitator = models.ForeignKey("users.User", related_name="has_invited")
  invited = models.ForeignKey("users.User", related_name="been_invited")

  class Meta:
    app_label = 'organizations'
    verbose_name = _('organization_invite')
