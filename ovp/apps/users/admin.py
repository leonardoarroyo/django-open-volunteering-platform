from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.users.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from django_extensions.admin import ForeignKeyAutocompleteAdmin

class UserResource(resources.ModelResource):
  user = Field()
  address = Field()
  state = Field()
  
  class Meta:
    model = User
    exclude = ('name', 'slug', 'channel', 'password', 'last_login', 'groups', 'user_permissions', 'uuid', 'locale', 'avatar', 'public', 'is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'is_subscribed_to_newsletter', 'joined_date', 'modified_date')
  
  def dehydrate_user (self, user):
    return user.name

  def dehydrate_address(self, user):
    if user.profile is not None and user.profile.address is not None:
      return user.profile.address.typed_address

  def dehydrate_state(self, user):
    if user.profile is not None and user.profile.address is not None:
      return user.profile.address.city_state.split(',')[-1]

class UserAdmin(ImportExportModelAdmin, ChannelModelAdmin, ForeignKeyAutocompleteAdmin):
  fields = [
    ('id', 'name', 'email'), 'slug', 'phone', 'password',
    ('is_staff','is_superuser','is_active','is_email_verified','public',),
    'groups'
  ]

  resource_class = UserResource

  list_display = [
    'id', 'email', 'name', 'last_login', 'is_active', 'is_staff', 'is_email_verified'
  ]

  list_filter = [
    'is_active', 'is_staff', 'last_login', 'joined_date'
  ]

  list_editable = [
    'is_active', 'is_staff', 'is_email_verified'
  ]

  search_fields = [
    'email', 'name'
  ]

  readonly_fields = ['id']
  raw_id_fields = []

admin_site.register(User, UserAdmin)
