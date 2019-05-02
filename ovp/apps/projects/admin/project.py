import os

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import TabularInline
from ovp.apps.projects.models import Project, VolunteerRole, Job, Work
from ovp.apps.organizations.models import Organization
from ovp.apps.core.models import GoogleAddress
from ovp.apps.core.models import SimpleAddress
from ovp.apps.organizations.admin import StateListFilter
from ovp.apps.organizations.admin import CityListFilter
from .job import JobInline
from .work import WorkInline

from ovp.apps.core.mixins import CountryFilterMixin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from jet.filters import RelatedFieldAjaxListFilter
from jet.filters import DateRangeFilter

class VolunteerRoleInline(TabularInline):
  model = VolunteerRole
  exclude = ['channel']

class ProjectResource(resources.ModelResource):
  id = Field(attribute='id', column_name='ID')
  name = Field(attribute='name', column_name='Nome do Projeto')
  description = Field(attribute='description', column_name='Descricao')
  causes = Field(column_name='Causas')
  organization_id = Field(column_name='ID ONG')
  organization = Field(column_name='ONG')
  address = Field(column_name='Endereço')
  link = Field(column_name='link')
  owner_id = Field(column_name='ID Responsavel')
  owner_name = Field(column_name='Nome Responsavel')
  owner_email = Field(column_name='Email Responsavel')
  owner_phone = Field(column_name='Telefone Responsavel')
  image = Field(column_name='Imagem')
  start_date = Field(column_name='Data de início')
  end_date = Field(column_name='Data de Encerramento')
  benefited_people = Field(attribute='benefited_people', column_name='Pessoas beneficiadas')
  disponibility = Field(column_name='Presencial ou a distancia')
  bookmark = Field(column_name='Número de curtidas')
  
  class Meta:
    model = Project
    fields = (
      'id',
      'name',
      'applied_count',
      'owner_id',
      'owner_name',
      'owner_email',
      'owner_phone',
      'organization_id',
      'organization', 
      'address',
      'image',
      'description',
      'link',
      'disponibility',
      'causes',
      'start_date',
      'end_date',
      'benefited_people',
      'published',
      'closed',
      'bookmark',
    )

  def dehydrate_organization(self, project):
    if project.organization:
      return project.organization.name

  def dehydrate_organization_id(self, project):
    if project.organization:
      return project.organization.id

  def dehydrate_causes(self, project):
    if project.causes:
      return ", ".join([c.name for c in project.causes.all()])

  def dehydrate_owner_id(self, project):
    if project.owner:
      return project.owner.id

  def dehydrate_owner_name(self, project):
    if project.owner:
      return project.owner.name

  def dehydrate_owner_email(self, project):
    if project.owner:
      return project.owner.email

  def dehydrate_owner_phone(self, project):
    if project.owner:
      return project.owner.phone

  def dehydrate_image(self, project):
    api_url = os.environ.get('API_URL', None) 
    if project.image:
      return api_url+project.image.image_large.url if api_url is not None \
        else project.image.image_large.url

  def dehydrate_start_date(self, project):
    try:
      job = Job.objects.filter(project=project)
      return job[0].start_date.strftime("%d/%m/%Y %H:%M:%S")
    except:
      return "recorrente"

  def dehydrate_end_date(self, project):
    try:
      job = Job.objects.filter(project=project)
      return job[0].end_date.strftime("%d/%m/%Y %H:%M:%S")
    except:
      return "recorrente"

  def dehydrate_address(self, project):
    if project.address is not None:
      if isinstance(project.address, GoogleAddress):
        return project.address.address_line
      if isinstance(project.address, SimpleAddress):
        return project.address.street + ', ' + project.address.number + ' - ' + project.address.neighbourhood + ' - ' + project.address.city

  def dehydrate_disponibility(self, project):
    try:
      return "A distância" if project.job.can_be_done_remotely else "Presencial"
    except:
      pass

    try:
      return "A distância" if project.work.can_be_done_remotely else "Presencial"
    except:
      pass

    return None

  def dehydrate_bookmark(self, project):
    return project.bookmark_count()

  def dehydrate_link(self, project):
    site_url = os.environ.get('SITE_URL', None)
    if site_url:
      return site_url + project.slug

    return project.slug


class ProjectAdmin(ImportExportModelAdmin, ChannelModelAdmin, CountryFilterMixin):

  list_filter = (
    ('organization', RelatedFieldAjaxListFilter),
    ('owner', RelatedFieldAjaxListFilter),
    ('address', RelatedFieldAjaxListFilter),
    ('image', RelatedFieldAjaxListFilter),
  )

  formfield_overrides = {
    models.TextField: {'widget': AdminMartorWidget},
  }

  fields = [
    ('id', 'highlighted'), ('name', 'slug'),
    ('organization', 'owner'),
    ('owner__name', 'owner__email', 'owner__phone'),

    ('applied_count', 'benefited_people'),
    ('volunteers__list'),
    ('can_be_done_remotely', 'skip_address_filter', 'chat_enabled'),

    ('published', 'closed', 'deleted', 'canceled'),
    ('published_date', 'closed_date', 'deleted_date', 'canceled_date'),

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
    ('created_date', DateRangeFilter), # fix: PONTUAL OU RECORRENTE
    'highlighted', 'published', 'closed', 'deleted', StateListFilter, CityListFilter, 'categories'
  ]

  list_editable = [
    'highlighted', 'published', 'closed'
  ]

  search_fields = [
    'name', 'organization__name'
  ]

  readonly_fields = [
    'id', 'created_date', 'modified_date', 'published_date', 'closed_date', 'deleted_date', 'canceled_date', 'applied_count', 'max_applies_from_roles',
    'owner__name', 'owner__email', 'owner__phone', 'can_be_done_remotely', 'volunteers__list'
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
    if isinstance(obj.address, GoogleAddress):
      return obj.address.city_state
    else:
      return ""
  
  def volunteers__list(self, obj):
    site_url = os.environ.get('ADMIN_URL', None)
    if site_url:
      return format_html("<a href='" + site_url + "admin/projects/apply/?q=" + obj.name + "' target='__blank'>Lista de Voluntários</a>")

    return ""

admin_site.register(Project, ProjectAdmin)
