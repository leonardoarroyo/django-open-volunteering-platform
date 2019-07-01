from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

class Post(ChannelRelationship):
  content = models.TextField(_('content'), max_length=3000)
  user = models.ForeignKey('users.User', verbose_name=_('user'))
  reply_to = models.ForeignKey('Post', verbose_name=_('reply'), blank=True, null=True)
  published = models.BooleanField('Published', default=True)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True)
  gallery = models.ForeignKey('gallery.Gallery', verbose_name=_('gallery'), blank=True, null=True)

  def save(self, *args, **kwargs):
    return super(Post, self).save(*args, **kwargs)

  def __str__(self):
    return "Post #{} - by {}".format(self.pk, self.user.name)
