from django import forms
from django.utils.translation import ugettext_lazy as _
from jet.filters import DateRangeFilter

from ovp.apps.admin.filters import SingleTextInputFilter
from ovp.apps.organizations.admin import StateListFilter as BaseStateListFilter
from ovp.apps.organizations.admin import CityListFilter as BaseCityListFilter
from ovp.apps.projects.models import Apply
from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.core.mixins import CountryFilterMixin
from ovp.apps.core.models import GoogleAddress
from ovp.apps.core.models import SimpleAddress
from ovp.apps.core.helpers import get_address_model

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

class ApplyResource(resources.ModelResource):
  organization = Field()
  address = Field()
  volunteer_name = Field()
  volunteer_email = Field()
  volunteer_phone = Field()
  project = Field()
  project_end_date = Field()

  class Meta:
    model = Apply
    fields = ('name', 'volunteer_name', 'volunteer_phone', 'volunteer_email', 'status', 'date', 'organization', 'project', 'project_end_date')

  def dehydrate_project_end_date(self, apply):
    if hasattr(apply.project, "job"):
      return apply.project.job.end_date

  def dehydrate_organization(self, apply):
    return apply.project.organization.name

  def dehydrate_project(self, apply):
    return apply.project.name

  def dehydrate_address(self, apply):
    if apply.project.address is not None:
      address = apply.project.address
      if isinstance(address, GoogleAddress):
        return address.address_line
      if isinstance(address, SimpleAddress):
        return address.street + ', ' + address.number + ' - ' + address.neighbourhood + ' - ' + address.city

  def dehydrate_volunteer_name(self, apply):
    if apply.user is not None:
      return apply.user.name

    return apply.username

  def dehydrate_volunteer_email(self, apply):
    if apply.user is not None:
      return apply.user.email

    return apply.email

  def dehydrate_volunteer_phone(self, apply):
    if apply.user is not None:
      return apply.user.phone

    return apply.phone


class StateListFilter(BaseStateListFilter):
    def queryset(self, request, queryset):
      address_model = get_address_model()
      state = request.GET.get('state', None)

      if state:
        if address_model == GoogleAddress:
          return queryset.filter(project__address__address_components__short_name=state, project__address__address_components__types__name="administrative_area_level_1")

        if address_model == SimpleAddress:
          return queryset.filter(project__address__state = state)
      return queryset


class CityListFilter(BaseCityListFilter):
    def queryset(self, request, queryset):
      address_model = get_address_model()
      city = request.GET.get('city', None)

      if city:
        if address_model == GoogleAddress:
          return queryset.filter(project__address__address_components__long_name=city, project__address__address_components__types__name="administrative_area_level_2")

        if address_model == SimpleAddress:
          return queryset.filter(project__address__city = city)
      return queryset

class ApplyAdmin(ChannelModelAdmin, CountryFilterMixin, ImportExportModelAdmin):
  resource_class = ApplyResource

  fields = [
    ('id', 'project__name', 'status'),
    'user', 'project', 'project__organization__name',
    ('canceled_date', 'date'),
    'email',
    'phone',
    'username'
  ]

  list_display = [
    'id', 'date', 'user__name', 'user__email', 'user__phone', 'project__name',
    'project__organization__name', 'project__address', 'username', 'phone', 'email', 'status'
  ]

  list_filter = [('date', DateRangeFilter), ('project__job__end_date', DateRangeFilter), 'status', StateListFilter, CityListFilter]

  list_editable = []

  search_fields = [
    'user__name', 'user__email', 'project__pk', 'project__name',
    'project__organization__name'
  ]

  readonly_fields = [
    'id', 'project__name', 'user', 'project__organization__name', 'canceled_date', 'date'
  ]

  raw_id_fields = []

  def user__name(self, obj):
    if obj.user:
      return obj.user.name
    else:
      return _('None')

  user__name.short_description = _('Name')
  user__name.admin_order_field = 'user__name'

  def user__email(self, obj):
    if obj.user:
      return obj.user.email
    else:
      return _('None')
  user__email.short_description = _('E-mail')
  user__email.admin_order_field = 'user__email'

  def user__phone(self, obj):
    if obj.user:
      return obj.user.phone
    else:
      return _('None')
  user__phone.short_description = _('Phone')
  user__phone.admin_order_field = 'user__phone'

  def project__name(self, obj):
    if obj.project:
      return obj.project.name
    else:
      return _('None')
  project__name.short_description = _('Project')
  project__name.admin_order_field = 'project__name'

  def project__organization__name(self, obj):
    if obj.project and obj.project.organization:
      return obj.project.organization.name
    else:
      return _('None')
  project__organization__name.short_description = _('Organization')
  project__organization__name.project__organization__name = 'project__organization__name'

  def project__address(self, obj):
    if obj.project:
      return obj.project.address
    else:
      return _('None')
  project__address.short_description = _('Address')
  project__address.admin_order_field = 'project__address'

  def get_queryset(self, request):
    qs = super(ApplyAdmin, self).get_queryset(request)
    return self.filter_by_country(request, qs, 'project__address')

admin_site.register(Apply, ApplyAdmin)
