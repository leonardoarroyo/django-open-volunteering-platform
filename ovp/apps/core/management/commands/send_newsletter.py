import sys

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db.models import Q

from ovp.apps.users.models import User
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Job
from ovp.apps.core.newsletter import Newsletter

class Command(BaseCommand):
  help = "Send newsletter automatic"
  projects = []
  def handle(self, *args, **options):
    for user in User.objects.all():
      skills = user.profile.skills.values_list('id', flat=True)
      causes = user.profile.causes.values_list('id', flat=True)
      
      criterion1 = Q(start_date__gt=timezone.now())
      criterion2 = Q(end_date__lte=timezone.now() + timezone.timedelta(days=7))
      criterion3 = Q(project__skills__in=skills)
      criterion4 = Q(project__causes__in=causes)
      criterion5 = Q(project__published=True)

      jobs = Job.objects.filter(criterion1 & criterion2 & criterion3 & criterion4 & criterion5)
      projects = [job.project for job in jobs]
      
      if len(projects):
        Newsletter(user).sendNewsletter({'projects': projects[:5]})