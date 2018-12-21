from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.users.models import User
from ovp.apps.core.models import GoogleAddress
from ovp.apps.core.models import SimpleAddress

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from django_extensions.admin import ForeignKeyAutocompleteAdmin

class UserResource(resources.ModelResource):  
  class Meta:
    model = User
    fields = (
      'id',
      'name',
      'email',
      'phone', 
    )


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
