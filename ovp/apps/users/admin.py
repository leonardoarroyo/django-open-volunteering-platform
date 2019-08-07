from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.admin.resources import CleanModelResource
from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.users.models import User
from ovp.apps.core.models import GoogleAddress
from ovp.apps.core.models import SimpleAddress

from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from django_extensions.admin import ForeignKeyAutocompleteAdmin
from jet.filters import DateRangeFilter

class UserResource(CleanModelResource):
  id = Field(attribute='id', column_name='ID')
  name = Field(attribute='name', column_name='Nome')
  email = Field(attribute='email', column_name='Email')
  phone = Field(attribute='phone', column_name='Telefone')
  address = Field(column_name='Endereço')
  city_state = Field(column_name='Cidade/Estado')
  causes = Field(column_name='Causas')
  joined_date = Field(attribute='joined_date', column_name='Data do cadastro')
  document = Field(attribute='document', column_name='Documento')
  has_done_volunteer_work_before = Field(attribute='has_done_volunteer_work_before')

  class Meta:
    model = User
    fields = (
      'id',
      'name',
      'email',
      'phone',
      'document',
      'address',
      'city_state',
      'causes',
      'joined_date',
    )

  def dehydrate_causes(self, user):
    if user.profile:
      return ", ".join([c.name for c in user.profile.causes.all()])

  def dehydrate_address(self, user):
    if user.profile is not None:
      if isinstance(user.profile.address, GoogleAddress):
        return user.profile.address.address_line
      if isinstance(user.profile.address, SimpleAddress):
        return user.profile.address.street + ', ' + user.profile.address.number + ' - ' + user.profile.address.neighbourhood + ' - ' + user.profile.address.city

  def dehydrate_city_state(self, user):
    if user.profile is not None:
      if isinstance(user.profile.address, GoogleAddress):
        return user.profile.address.city_state
      if isinstance(user.profile.address, SimpleAddress):
        return user.profile.address.city

  def dehydrate_has_done_volunteer_work_before(self, user):
    if user.profile is not None:
      return user.profile.has_done_volunteer_work_before
    return None


class UserAdmin(ImportExportModelAdmin, ChannelModelAdmin, ForeignKeyAutocompleteAdmin):
  fields = [
    ('id', 'name', 'email'), 'slug', 'phone', 'password', 'document',
    ('is_staff','is_superuser','is_active','is_email_verified','public',),
    'groups',
    'flairs',
    'has_done_volunteer_work_before'
  ]

  resource_class = UserResource

  list_display = [
    'id', 'email', 'name', 'last_login', 'is_active', 'is_staff', 'is_email_verified'
  ]

  list_filter = [
    'is_active', 'is_staff', ('joined_date', DateRangeFilter)
  ]

  list_editable = [
    'is_active', 'is_staff', 'is_email_verified'
  ]

  search_fields = [
    'email', 'name'
  ]

  readonly_fields = ['id', 'has_done_volunteer_work_before']
  raw_id_fields = []

  def has_done_volunteer_work_before(self, user):
    v = None
    if user.profile is not None:
      v = user.profile.has_done_volunteer_work_before
    return v if v else "Undefined"

admin_site.register(User, UserAdmin)
