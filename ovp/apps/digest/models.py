import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from ovp.apps.channels.models.abstract import ChannelRelationship

PROJECT = 1


class DigestLog(ChannelRelationship):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient = models.CharField('Recipient email', max_length=300)
    context = JSONField('Context', blank=True, null=True)
    campaign = models.IntegerField('Campaign', blank=True, null=True)
    trigger_date = models.DateTimeField(auto_now_add=True)


CT_CHOICES = (
    (PROJECT, 'Project'),
)


class DigestLogContent(ChannelRelationship):
    digest_log = models.ForeignKey('DigestLog', on_delete=models.DO_NOTHING)
    content_type = models.IntegerField('Content type', choices=CT_CHOICES)
    content_id = models.IntegerField('Content id')

class DigestText(ChannelRelationship):
    text_content = models.TextField('Conteúdo', blank=True, null=True)
    default_content = models.TextField('Default context', blank=True, null=True)
    keep_text = models.BooleanField('Manter conteúdo após envio', default=False)

    def __str__(self):
        return "Conteúdo da newsletter"
