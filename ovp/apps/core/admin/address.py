from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.core.models import GoogleAddress

from django_extensions.admin import ForeignKeyAutocompleteAdmin

class GoogleAddressAdmin(ChannelModelAdmin, ForeignKeyAutocompleteAdmin):
  fields = [
    'id', 'typed_address', 'typed_address2'
  ]

  list_display = [
    'id', 'typed_address', 'typed_address2'
  ]

  list_filter = []

  list_editable = []

  search_fields = ['typed_address', 'typed_address2', 'address_line']

  readonly_fields = [
    'id'
  ]

  raw_id_fields = []


admin_site.register(GoogleAddress, GoogleAddressAdmin)
