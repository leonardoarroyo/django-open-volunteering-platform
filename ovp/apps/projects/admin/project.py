from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from martor.widgets import AdminMartorWidget

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import TabularInline
from ovp.apps.projects.models import Project, VolunteerRole
from ovp.apps.organizations.models import Organization
from ovp.apps.organizations.admin import StateListFilter
from .job import JobInline
from .work import WorkInline

from ovp.apps.core.mixins import CountryFilterMixin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from jet.filters import RelatedFieldAjaxListFilter

class VolunteerRoleInline(TabularInline):
  model = VolunteerRole
  exclude = ['channel']

class ProjectResource(resources.ModelResource):
  organization = Field()
  address = Field()
  
  class Meta:
    model = Project
    fields = ('name', 'applied_count', 'organization', 'address', 'highlighted', 'published', 'closed', 'deleted')
    
  def dehydrate_organization(self, project):
    return project.organization.name

  def dehydrate_address(self, project):
    if project.address is not None:
      return project.address.typed_address

class ProjectAdmin(ImportExportModelAdmin, ChannelModelAdmin, CountryFilterMixin):

  list_filter = (
    ('organization', RelatedFieldAjaxListFilter),
    ('owner', RelatedFieldAjaxListFilter),
    ('address', RelatedFieldAjaxListFilter),
  )

  formfield_overrides = {
    models.TextField: {'widget': AdminMartorWidget},
  }

  fields = [
    ('id', 'highlighted'), ('name', 'slug'),
    ('organization', 'owner'),
    ('owner__name', 'owner__email', 'owner__phone'),

    ('applied_count'),

    ('can_be_done_remotely', 'skip_address_filter'),

    ('published', 'closed', 'deleted'),
    ('published_date', 'closed_date', 'deleted_date'),

    'address',
    'image',
    'categories',

    ('created_date', 'modified_date'),

    'description', 'details',
    'skills', 'causes',
    ]

  resource_class = ProjectResource 

  list_display = [
    'id', 'created_date', 'name', 'highlighted', 'published', 'closed', 'organization__name', 'city_state', 'applied_count', # fix: CIDADE, PONTUAL OU RECORRENTE
    'deleted', #fix: EMAIL STATUS
    ]

  list_filter = [
    'created_date', # fix: PONTUAL OU RECORRENTE
    'highlighted', 'published', 'closed', 'deleted', StateListFilter
  ]

  list_editable = [
    'highlighted', 'published', 'closed'
  ]

  search_fields = [
    'name', 'organization__name'
  ]

  readonly_fields = [
    'id', 'created_date', 'modified_date', 'published_date', 'closed_date', 'deleted_date', 'applied_count', 'max_applies_from_roles',
    'owner__name', 'owner__email', 'owner__phone',
    'can_be_done_remotely'
  ]

  raw_id_fields = []

  filter_horizontal = ('skills', 'causes',)

  inlines = [
    VolunteerRoleInline,
    JobInline, WorkInline
  ]

  #def Resource(model, **kwargs):
    

  def can_be_done_remotely(self, obj):
    if obj.hasattr('job') and obj.job:
      return obj.job.can_be_done_remotely
    elif obj.hasattr('work') and obj.work:
      return obj.job.can_be_done_remotely
    else:
      return _('Type not specified')
  can_be_done_remotely.short_description = _('Can be done remotely?')

  def organization__name(self, obj):
    if obj.organization:
      return obj.organization.name
    else:
      return _('None')
  organization__name.short_description = _('Organization')
  organization__name.admin_order_field = 'organization__name'

  def owner__name(self, obj):
    return obj.owner and obj.owner.name or _('Owner not assigned')
  owner__name.short_description = _('Owner name')
  owner__name.admin_order_field = 'owner__name'

  def owner__email(self, obj):
    return obj.owner and obj.owner.email or _('Owner not assigned')
  owner__email.short_description = _('Owner email')
  owner__email.admin_order_field = 'owner__email'

  def owner__phone(self, obj):
    return obj.owner and obj.owner.phone or _('Owner not assigned')
  owner__phone.short_description = _('Owner phone')
  owner__phone.admin_order_field = 'owner__phone'

  def get_queryset(self, request):
    qs = super(ProjectAdmin, self).get_queryset(request)
    return self.filter_by_country(request, qs, 'address')

  def city_state(self, obj):
    if obj.address is not None:
      return obj.address.city_state

admin_site.register(Project, ProjectAdmin)
