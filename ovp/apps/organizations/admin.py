from django import forms
from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from django.utils.translation import ugettext_lazy as _

from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project
from ovp.apps.core.models import AddressComponent

from ovp.apps.projects.models import Project

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.core.mixins import CountryFilterMixin
from ovp.apps.organizations import validators
from ovp.apps.core.models import GoogleAddress
from ovp.apps.core.models import SimpleAddress
from ovp.apps.core.helpers import get_address_model

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from jet.filters import RelatedFieldAjaxListFilter
from jet.filters import DateRangeFilter

# This file contains some "pragma: no cover" because the admin
# class is not covered by the test suite

class OrganizationResource(resources.ModelResource):
  id = Field(attribute='id', column_name='ID')
  name = Field(attribute='name', column_name='Nome do Projeto')
  description = Field(attribute='description', column_name='Descricao')
  document = Field(attribute='document', column_name='CNPJ')
  owner_name = Field(column_name='Nome Responsavel')
  owner_email = Field(column_name='Email Responsavel')
  owner_phone = Field(column_name='Telefone Responsavel')
  address = Field(column_name='Endereço')
  city_state = Field(column_name='Cidade/Estado')
  causes = Field(column_name='Causas')
  image = Field(column_name='Imagem')
  volunteers = Field(column_name='Número de Voluntários')
  website = Field(attribute='website', column_name='Site')
  facebook_page = Field(attribute='facebook_page', column_name='Facebook')
  created_project = Field(column_name='Ong já criou ação?')
  benefited_people = Field(attribute='benefited_people', column_name='Pessoas beneficiadas')
  rating = Field(attribute='rating', column_name='Avaliação')

  class Meta:
    model = Organization
    fields = (
      'id',
      'name',
      'owner_name',
      'owner_email', 
      'owner_phone',
      'address',
      'city_state',
      'image',
      'facebook_page',
      'website',
      'document',
      'causes',
      'published',
      'deleted',
      'created_date',
      'created_project',
      'benefited_people',
      'rating',
    )

  def dehydrate_address(self, organization):
    if organization.address is not None:
      if isinstance(organization.address, GoogleAddress):
        return organization.address.address_line
      if isinstance(organization.address, SimpleAddress):
        return organization.address.street + ', ' + organization.address.number + ' - ' + organization.address.neighbourhood + ' - ' + organization.address.city

  def dehydrate_owner_name(self, organization):
    return organization.owner.name

  def dehydrate_owner_email(self, organization):
    return organization.owner.email

  def dehydrate_owner_phone(self, organization):
    return organization.owner.phone

  def dehydrate_causes(self, organization):
    if organization.causes:
      return ", ".join([c.name for c in organization.causes.all()])

  def dehydrate_volunteers(self, organization):
    project = Project.objects.filter(organization=organization)
    total = 0
    for p in project:
      total += p.applied_count

    return total

  def dehydrate_created_project(self, organization):
    projects = Project.objects.filter(organization=organization)
    if len(projects) > 0:
      return "Sim"

    return "Não"

  def dehydrate_city_state(self, organization):
    if organization.address is not None:
      if isinstance(organization.address, GoogleAddress):
        return organization.address.city_state
      if isinstance(organization.address, SimpleAddress):
        return organization.address.city

class StateListFilter(admin.SimpleListFilter):
    title = 'state'
    parameter_name = 'state'

    def lookups(self, request, model_admin):
      address_model = get_address_model()

      if address_model == GoogleAddress:
        states = AddressComponent.objects.filter(channel__slug=request.channel, types__name="administrative_area_level_1").values_list('short_name', flat=True).distinct()

      if address_model == SimpleAddress:
        states = SimpleAddress.objects.filter(channel__slug=request.channel).values_list('state', flat=True).distinct()

      return [('', 'No state')] + [(x, x) for x in states]

    def queryset(self, request, queryset):
      address_model = get_address_model()
      state = request.GET.get('state', None)

      if state:
        if address_model == GoogleAddress:
          return queryset.filter(address__address_components__short_name=state, address__address_components__types__name="administrative_area_level_1")

        if address_model == SimpleAddress:
          return queryset.filter(address__state = state)
      return queryset


class CityListFilter(admin.SimpleListFilter):
    title = 'city'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
      address_model = get_address_model()

      if address_model == GoogleAddress:
        states = AddressComponent.objects.filter(channel__slug=request.channel, types__name="administrative_area_level_2").values_list('long_name', flat=True).distinct()

      if address_model == SimpleAddress:
        states = SimpleAddress.objects.filter(channel__slug=request.channel).values_list('city', flat=True).distinct()

      return [('', 'No city')] + [(x, x) for x in states]

    def queryset(self, request, queryset):
      address_model = get_address_model()
      city = request.GET.get('city', None)

      if city:
        if address_model == GoogleAddress:
          return queryset.filter(address__address_components__long_name=city, address__address_components__types__name="administrative_area_level_2")

        if address_model == SimpleAddress:
          return queryset.filter(address__city = city)
      return queryset

class OrganizationAdmin(ImportExportModelAdmin, ChannelModelAdmin, CountryFilterMixin):

  formfield_overrides = {
    models.TextField: {'widget': AdminMartorWidget},
  }

  fields = [
    ('id', 'highlighted'), ('name', 'slug'),
    ('owner'), #- 'type'

    ('published', 'deleted', 'verified'),
    ('published_date', 'deleted_date'),
    'rating',
    'benefited_people',
    'address',
    'image',
    'document',
    'contact_name',
    'contact_phone',
    'contact_email',
    'categories',

    'facebook_page', 'website',

    'description', 'details',
    'causes',

    ('created_date', 'modified_date'),
    ]

  resource_class = OrganizationResource

  list_display = [
    'id', 'created_date', 'name', 'published', 'highlighted', 'owner__email', 'owner__phone', 'city_state', 'volunteers', 'address', 'rating', 'modified_date', 'deleted'
  ]

  list_filter = [
    ('created_date', DateRangeFilter), ('modified_date', DateRangeFilter), 'highlighted', 'published', 'deleted', StateListFilter, CityListFilter
  ]

  list_editable = [
    'highlighted', 'published'
  ]

  search_fields = [
    'name', 'owner__email', 'address__typed_address', 'description'
  ]

  readonly_fields = ['id', 'created_date', 'modified_date', 'published_date', 'deleted_date', 'rating']


  filter_horizontal = ('causes', 'members')

  def queryset(self, request):
      qs = super(OrganizationAdmin, self).queryset(request)
      return qs.annotate(city="SP")

  def owner__name(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.name
    else:
      return _('None')
  owner__name.short_description = _("Owner's Name")
  owner__name.admin_order_field = 'owner__name'

  def owner__email(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.email
    else:
      return _('None')
  owner__email.short_description = _("Owner's E-mail")
  owner__email.admin_order_field = 'owner__email'

  def owner__phone(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.phone
    else:
      return _('None')
  owner__phone.short_description = _("Owner's Phone")
  owner__phone.admin_order_field = 'owner__phone'

  def volunteers(self, obj):
    project = Project.objects.filter(organization=obj)
    total = 0
    for p in project:
      total += p.applied_count

    return total

  def city_state(self, obj):
    if obj.address is not None:
      return obj.address.city_state

  def get_queryset(self, request): #pragma: no cover
    qs = super(OrganizationAdmin, self).get_queryset(request)
    return self.filter_by_country(request, qs, 'address')


admin_site.register(Organization, OrganizationAdmin)
