from django.utils import timezone
from django.db import transaction
from ovp.apps.organizations.models import Organization
from django.db.models.signals import post_save
from django.conf import settings
from .tasks import push_organization

def store_on_sf(sender, *args, **kwargs):
    instance = kwargs["instance"]
    channel = instance.channel.slug
    integration_data = getattr(settings, 'SALESFORCE_INTEGRATION',{})
    channel_integration = integration_data.get(channel, None)

    if kwargs["raw"] or not channel_integration or not channel_integration.get('enabled', False):
        return None

    # Only store published organizations
    if not instance.published:
        return None

    transaction.on_commit(lambda: push_organization.apply_async(
        kwargs={"organization_pk": instance.pk},
    ))
post_save.connect(store_on_sf, sender=Organization)
