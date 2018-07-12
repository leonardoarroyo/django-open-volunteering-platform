from ovp.apps.channels.viewsets.decorators import ChannelViewSet

import csv
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Count


from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response

from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project, Apply
from ovp.apps.users.models import User


@ChannelViewSet
class AnalyticsResourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  AnalyticsResourceViewSet resource endpoint
  """
  def list(self, request):
    if not request.user.is_staff:
      raise PermissionDenied

    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    try:
      # Convert query params start_date and end_date to datetime
      start_date = datetime.strptime(start_date_param, '%d/%m/%Y')
      end_date = datetime.strptime(end_date_param, '%d/%m/%Y') if end_date_param else timezone.now()
    except ValueError:
      return response.Response("Datas inválidas")

    organizations_count = Organization.objects.filter(
      created_date__gte=start_date,
      created_date__lte=end_date
    ).count()
    organizations_published_count = Organization.objects.filter(
      published_date__gte=start_date,
      published_date__lte=end_date
    ).count()
    projects_count = Project.objects.filter(
      created_date__gte=start_date,
      created_date__lte=end_date
    ).count()
    projects_published_count = Project.objects.filter(
      published_date__gte=start_date,
      published_date__lte=end_date,
    ).count()
    users_count = User.objects.filter(
      joined_date__gte=start_date,
      joined_date__lte=end_date
    ).count()
    applies_count = Apply.objects.filter(
      date__gte=start_date,
      date__lte=end_date
    ).count()
    applies_distinct_count = Apply.objects.filter(
      date__gte=start_date,
      date__lte=end_date
    ).values('user_id').annotate(total=Count('user_id')).count()

    http_response = HttpResponse(content_type='text/csv')
    http_response['Content-Disposition'] = 'attachment; filename="analytics.csv"'

    csv_writer = csv.writer(http_response)

    csv_writer.writerow(['Relatório referente a {0} até {1}'.format(
      start_date_param,
      end_date_param
    )])
    csv_writer.writerow([])
    csv_writer.writerow(['Organizações criadas:', organizations_count])
    csv_writer.writerow(['Organizações publicadas:', organizations_published_count])
    csv_writer.writerow(['Vagas criadas:', projects_count])
    csv_writer.writerow(['Vagas publicadas:', projects_published_count])
    csv_writer.writerow(['Usuários cadastrados:', users_count])
    csv_writer.writerow(['Usuários inscritos em vagas:', applies_distinct_count])
    csv_writer.writerow(['Inscrições em vagas:', applies_count])

    return http_response

  def get_serializer_class(self):
    print(self.action)
