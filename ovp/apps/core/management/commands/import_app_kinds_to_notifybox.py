import re
import os
import collections
import logging
import json
from operator import itemgetter
from typing import List
from django.template.loaders.app_directories import get_app_template_dirs
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.staticfiles import finders
from ovp.apps.core.notifybox import NotifyBoxApi
from ovp.apps.users.models.profile import get_profile_model
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from ovp.apps.channels.models import ChannelSetting

kinds = ["applicationConfirmed", "applicationCanceled", "applicationCreated", "applicationReminder", "ratingRequested"]

def import_kinds(channel: str):
    """ Import email templates to notifybox
    """
    access_key = ChannelSetting.objects.get(channel__slug = channel, key="NOTIFYBOX_ACCESS_KEY").value
    secret_key = ChannelSetting.objects.get(channel__slug = channel, key="NOTIFYBOX_SECRET_KEY").value
    client = NotifyBoxApi(access_key, secret_key)

    for kind in kinds:
        kind_id, kind_value = itemgetter('id', 'value')(client.getOrCreateKind(kind))
        template = client.createOrUpdateTemplate(kind_id, 'app', 'default', 'pt-br', "{}", "")
        trigger = client.createOrUpdateTrigger(kind_id, template["id"], 'default', 'app')

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'channel',
            help='Channel slug',
            type=str,
        )

    def handle(self, *args, **options):
        # Converts value from verbosity int to logging library
        # level.
        # 1 -> 30 (logging.WARNING)
        # 2 -> 20 (logging.INFO)
        # 3 -> 10 (logging.DEBUG)
        loggingLevel = 40 - (options['verbosity'] * 10)

        logger = logging.getLogger()
        console = logging.StreamHandler()

        logger.setLevel(loggingLevel)
        console.setLevel(loggingLevel)

        logger.addHandler(console)

        import_kinds(options['channel'])
