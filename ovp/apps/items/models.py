from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models import ChannelRelationship

from ckeditor.fields import RichTextField

class Item(ChannelRelationship):
  """
  Item model
  """
  name = models.CharField(_('Item name'), max_length=100)
  imageable = models.CharField(_('Imageable name'), blank=True, null=True, max_length=100)
  imageable_id = models.IntegerField(_('Imageable id'), blank=True, null=True, default=0)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True)

  def save(self, *args, **kwargs):
    self.modified_date = timezone.now()
    super(Item, self).save(*args, **kwargs)

  class Meta:
    app_label = 'items'
    verbose_name = _('item')
    verbose_name_plural = _('items')


class ItemImage(ChannelRelationship):
  """
  ItemImage model
  """
  image = models.ForeignKey('uploads.UploadedImage', blank=False, null=False, verbose_name=_('image'))
  item = models.ForeignKey('Item', models.CASCADE, blank=True, null=True, verbose_name=_('item'))
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True)

  def save(self, *args, **kwargs):
    self.modified_date = timezone.now()
    super(ItemImage, self).save(*args, **kwargs)

  class Meta:
    app_label = 'items'
    verbose_name = _('item image')
    verbose_name_plural = _('item images')


class ItemDocument(ChannelRelationship):
  """
  ItemDocument model
  """
  document = models.ForeignKey('uploads.UploadedDocument', blank=False, null=False, verbose_name=_('document'))
  item = models.ForeignKey('Item', models.CASCADE, blank=True, null=True, verbose_name=_('item'))
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True)
  about = RichTextField(_('About'), max_length=3000)

  def save(self, *args, **kwargs):
    self.modified_date = timezone.now()
    return super(ItemDocument, self).save(*args, **kwargs)
    
  class Meta:
    app_label = 'items'
    verbose_name = _('item document')
    verbose_name_plural = _('item documents')
