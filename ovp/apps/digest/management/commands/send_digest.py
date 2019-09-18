from ovp.apps.digest.digest import get_email_list
from ovp.apps.digest.digest import send_campaign
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, *args, **options):
    send_campaign(chunk_size=1000)
