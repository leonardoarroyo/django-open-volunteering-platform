from django.db import models
from django.utils.translation import ugettext_lazy as _
from ovp.apps.channels.models.abstract import ChannelRelationship

class ApplyStatusHistory(ChannelRelationship):
    apply = models.ForeignKey('projects.Apply')
    status = models.CharField(
        _('status'),
        max_length=30
    )
    date = models.DateTimeField(
        _("Status date"),
        auto_now_add=True
    )
