from django.db import models
from django.utils.translation import ugettext_lazy as _

class Channel(models.Model):
	name = models.CharField(_('Name'), max_length=100)

class ChannelRelationship(models.Model):
  channels = models.ManyToManyField(Channel, related_name="%(class)s_channels")

  class Meta:
    abstract = True

  def save(self, *args, **kwargs):
    creating = False
    if not self.pk:
      creating = True

    super(ChannelRelationship, self).save(*args, **kwargs)

    if creating:
      self.channels.add(Channel.objects.get(name="default"))
