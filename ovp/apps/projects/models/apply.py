from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver

from ovp.apps.projects import emails

from ovp.apps.channels.models.abstract import ChannelRelationship


apply_status_choices = (
    ('applied', 'Applied'),
    #('unapplied', 'Canceled'),
    #('not-volunteer', 'Not a Volunteer'),
    ('unapplied-by-volunteer', 'Canceled by volunteer'),
    ('unapplied-by-organization', 'Canceled by organization'),
    ('confirmed-volunteer', 'Confirmed Volunteer'),
)


class Apply(ChannelRelationship):

    user = models.ForeignKey(
        'users.User',
        blank=True,
        null=True,
        verbose_name=_('user')
    )
    project = models.ForeignKey('projects.Project', verbose_name=_('project'))
    status = models.CharField(
        _('status'),
        max_length=30,
        choices=apply_status_choices,
        default="applied"
    )
    role = models.ForeignKey(
        'projects.VolunteerRole',
        verbose_name=_('role'),
        blank=False,
        null=True
    )
    date = models.DateTimeField(
        _('created date'),
        auto_now_add=True,
        blank=True
    )
    canceled_date = models.DateTimeField(
        _("canceled date"),
        blank=True,
        null=True
    )

    username = models.CharField(
        _('name'),
        max_length=200,
        blank=True,
        null=True
    )
    email = models.CharField(_('email'), max_length=190, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, null=True)
    document = models.CharField(
        _('Documento'),
        max_length=100,
        blank=True,
        null=True
    )
    message = models.TextField(
        _('message'),
        max_length=3000,
        blank=True,
        null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def mailing(self, async_mail=None):
        return emails.ApplyMail(self, async_mail)

    def save(self, *args, **kwargs):
        creating = self.id is None

        # Set canceled date if status is unapplied
        self._save__set_canceled_status(creating)

        # Save
        return_data = super().save(*args, **kwargs)

        # Emails and history
        #if creating and self.project.closed is False:
        #    self.mailing().sendAppliedToVolunteer({'apply': self})
        #    self.mailing().sendAppliedToOwner({'apply': self})
        #else:
        #    if (self.__original_status != self.status
        #            and self.status == "unapplied"
        #            and self.project.closed is False):
        #        self.mailing().sendUnappliedToVolunteer({'apply': self})
        #        self.mailing().sendUnappliedToOwner({'apply': self})

        # Update original values
        self.__original_status = self.status
        return return_data

    def _save__set_canceled_status(self, creating):
        if not creating and self.__original_status != self.status:
            if self.status in ["unapplied-by-volunteer", "unapplied-by-organization"]:
                self.canceled_date = timezone.now()
            else:
                self.canceled_date = None

    class Meta:
        app_label = 'projects'
        verbose_name = _('apply')
        verbose_name_plural = _('applies')
        unique_together = (("email", "project"), )

@receiver(post_save, sender=Apply)
def set_applied_count(sender, **kwargs):
    if not kwargs.get('raw', False):
        instance = kwargs['instance']
        if instance.role:
            instance.role.applied_count = instance.role.get_volunteers_numbers()
            instance.role.save()
        instance.project.applied_count = instance.project.get_volunteers_numbers()
        instance.project.save()

class ApplyStatusHistory(models.Model):
    apply = models.ForeignKey('projects.Apply')
    status = models.CharField(
        _('status'),
        max_length=30,
        choices=apply_status_choices
    )
    date = models.DateTimeField(
        _("Status date"),
        auto_now_add=True
    )
