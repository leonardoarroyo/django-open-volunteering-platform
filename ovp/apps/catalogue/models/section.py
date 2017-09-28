from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.models.abstract import ChannelRelationship

from ovp.apps.catalogue.models.filter import CategoryFilter

CATEGORY = "CATEGORY"

FILTER_TYPES = (
  (CATEGORY, "Category"),
)

class Section(ChannelRelationship):
  catalogue = models.ForeignKey("catalogue.Catalogue", related_name="sections")
  name = models.CharField(_("Name"), max_length=100)
  slug = models.SlugField(_("Slug"), max_length=100)
  amount = models.IntegerField(_("Amount"), default=20)

  def __str__(self):
    return self.name

class SectionFilter(ChannelRelationship):
  section = models.ForeignKey("catalogue.Section", related_name="filters")
  type = models.CharField(_("Filter type"), max_length=30, choices=FILTER_TYPES)

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
  object_id = models.PositiveIntegerField(blank=True, null=True)
  filter = GenericForeignKey()

  def __str__(self):
    filter_name = self.filter.__str__()
    if filter_name != "None":
      return filter_name

    return "Empty filter"

  def save(self, *args, **kwargs):
    if not self.pk:
      self.create_filter_object(**kwargs)

    super(SectionFilter, self).save(*args, **kwargs)

  def create_filter_object(self, **kwargs):
    if self.type == CATEGORY:
      self.filter = CategoryFilter.objects.create(object_channel=kwargs.get("object_channel"))
