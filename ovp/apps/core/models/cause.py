import vinaigrette

from ovp.apps.channels.models import Channel
from ovp.apps.channels.models.abstract import ChannelRelationship

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Default causes
causes = ['Professional Training', 'Fight Poverty', 'Conscious consumption', 'Culture, Sport and Art', 'Human Rights', 'Education', 'Youth', 'Elders', 'Environment', 'Citizen Participation', 'Animal Protection', 'Health', 'People with disabilities']

class Cause(ChannelRelationship):
  name = models.CharField('name', max_length=100)
  image = models.ForeignKey('uploads.UploadedImage', blank=True, null=True, verbose_name=_('image'))

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'core'
    verbose_name = _('cause')

@receiver(post_save, sender=Channel)
def create_default_skills(sender, instance, **kwargs):
  for cause in causes:
    Cause.objects.create(name=cause, object_channel=instance.slug)

vinaigrette.register(Cause, ['name'])
