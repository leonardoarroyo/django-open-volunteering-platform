import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from jet.dashboard.modules import RecentActions
from jet.dashboard.modules import DashboardModule
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project, Apply
from ovp.apps.users.models import User
# from channels.pv.models import PVUserInfo

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
      #able_to_apply = PVUserInfo.objects.filter(can_apply=True)

      self.organizations_count = organizations.count()
      self.organizations_published_count = organizations.filter(published=True).count()
      self.projects_count = projects.count()
      self.projects_published_count = projects.filter(published=True).count()
      self.users_count = User.objects.count()
      #self.users_can_apply_count = able_to_apply.count()
      self.applies_count = Apply.objects.count()

      # Monthly
      now = timezone.now()
      day_one_month_before = (now - datetime.timedelta(365/12)).replace(tzinfo=timezone.utc)
      month_organizations = organizations.filter(created_date__gte=day_one_month_before)
      month_projects = projects.filter(created_date__gte=day_one_month_before)
      month_users = User.objects.filter(joined_date__gte=day_one_month_before)

      self.month_organizations_count = month_organizations.count()
      self.month_organizations_published_count = month_organizations.filter(published=True).count()
      self.month_projects_count = month_projects.count()
      self.month_projects_published_count = month_projects.filter(published=True).count()
      self.month_users_count = month_users.count()
      #self.month_users_can_apply_count = month_users.filter(pvuserinfo__in=able_to_apply).count()
      #self.month_applies_count = Apply.objects.filter(date__gte=day_one_month_before).count()

