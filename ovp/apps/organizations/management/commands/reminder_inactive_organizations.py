# -*- coding: utf-8 -*-
import sys

from django.db.models import Q
from django.core.management.base import BaseCommand
from django.utils import timezone

from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project

class Command(BaseCommand):
  help = "Reminder for organizations that do not create projects for more than 3 months"

  def handle(self, *args, **options):
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=90)

    criterion1 = Q(created_date__range=(start_date, end_date))
    criterion2 = Q(closed=True)

    organizations = Project \
              .objects \
              .values_list('organization', flat=True) \
              .exclude(criterion1 | criterion2) \
              .distinct()

    print("Inactive {} organizations".format(organizations.count()))
              
    for i in organizations:
        organization = Organization.objects.get(pk=i)
        organization.admin_mailing().sendOrganizationReminder({"organization": organization})