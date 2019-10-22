from ovp.apps.digest.digest import get_email_list
from ovp.apps.digest.digest import send_campaign
from ovp.apps.digest.models import DigestLog
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, *args, **options):
    sent = set(DigestLog.objects.filter(campaign=1).values_list('recipient', flat=True))
    all_emails = get_email_list()
    to_send = filter(lambda x: x not in sent, all_emails)
    send_campaign(chunk_size=1000, email_list=to_send)

