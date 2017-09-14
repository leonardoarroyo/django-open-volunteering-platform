from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.users.models import User


class UserAdmin(ChannelModelAdmin):
  fields = [
    ('id', 'name', 'email'), 'slug', 'phone',
    ('is_staff','is_superuser','is_active','is_email_verified','public',)
    ]

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
