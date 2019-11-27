from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
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

@receiver(post_save, sender=ApplyStatusHistory)
def set_applied_count(sender, **kwargs):
    if not kwargs.get('raw', False) and kwargs.get('created', True):
        apply = kwargs['instance'].apply

        # Emails and history
        if not apply.project.closed:
            if apply.status == "applied":
                apply.mailing().sendAppliedToVolunteer({'apply': apply})
                apply.mailing().sendAppliedToOwner({'apply': apply})
            if apply.status == "unapplied-by-volunteer":
                apply.mailing().sendUnappliedByVolunteerToVolunteer({'apply': apply})
                apply.mailing().sendUnappliedByVolunteerToOwner({'apply': apply})
            if apply.status == "unapplied-by-organization":
                apply.mailing().sendUnappliedByOrganizationToVolunteer({'apply': apply})
                apply.mailing().sendUnappliedByOrganizationToOwner({'apply': apply})
            if apply.status == "confirmed-volunteer":
                apply.mailing().sendConfirmedVolunteerToVolunteer({'apply': apply})
                apply.mailing().sendConfirmedVolunteerToOwner({'apply': apply})
