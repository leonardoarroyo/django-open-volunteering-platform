from psycopg2.extras import Json
from django.contrib.postgres.fields import JSONField
from ovp.apps.channels.models.abstract import ChannelRelationship

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Pixel(ChannelRelationship):
    source = models.CharField(_('source'), max_length=100)
    meta = JSONField(_('meta'))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'core'
        verbose_name = _('pixel')
