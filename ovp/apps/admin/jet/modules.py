from jet.dashboard.modules import RecentActions
from jet.dashboard.modules import DashboardModule
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project
from ovp.apps.users.models import User

class OVPRecentActions(RecentActions):
  def init_with_context(self, context):
    def get_qset(list):
      qset = None
      for contenttype in list:
        try:
          app_label, model = contenttype.split('.')

          if model == '*':
            current_qset = Q(
              content_type__app_label=app_label
            )
          else:
            current_qset = Q(
              content_type__app_label=app_label,
              content_type__model=model
            )
        except:
          raise ValueError('Invalid contenttype: "%s"' % contenttype)

        if qset is None:
          qset = current_qset
        else:
          qset = qset | current_qset
      return qset

    qs = LogEntry.objects

    if self.user:
      qs = qs.filter(
        user__pk=int(self.user)
      )

    if self.include_list:
      qs = qs.filter(get_qset(self.include_list))
    if self.exclude_list:
      qs = qs.exclude(get_qset(self.exclude_list))

    qs = qs.filter(user__channel=context["user"].channel)

    self.children = qs.select_related('content_type', 'user')[:int(self.limit)]


class Indicators(DashboardModule):
    title = "Indicators"
    title_url = "#"
    template = "admin/indicators.html"

    def init_with_context(self, context):
      organizations = Organization.objects.filter(deleted=False)
      projects = Project.objects.filter(deleted=False)
      self.organizations = "{}/{}".format(organizations.filter(published=True).count(), organizations.count())
      self.projects = "{}/{}".format(projects.filter(published=True, closed=False).count(), projects.count())
      self.users = User.objects.all().count()