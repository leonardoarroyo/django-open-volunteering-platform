from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.projects.models.category import Category

class CategoryAdmin(ChannelModelAdmin):
  list_display = ['id', 'name', 'newsletter']
  fields = ["name", "slug", "description", "image", "highlighted", "newsletter"]
  list_editable = ['newsletter']

admin_site.register(Category, CategoryAdmin)
