import vinaigrette

from ovp.apps.channels.models import Channel
from ovp.apps.channels.models.abstract import ChannelRelationship

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Default skills
skills = ['Arts/Handcrafting', 'Communication', 'Dance/Music', 'Law', 'Education', 'Sports', 'Cooking', 'Management', 'Idioms', 'Computers/Technology', 'Health', 'Others']

class Skill(ChannelRelationship):
  name = models.CharField(_('name'), max_length=100)

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'core'
    verbose_name = _('skill')

@receiver(post_save, sender=Channel)
def create_default_skills(sender, instance, **kwargs):
  for skill in skills:
    Skill.objects.create(name=skill, object_channel=instance.slug)

vinaigrette.register(Skill, ['name'])
