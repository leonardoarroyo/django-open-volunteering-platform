from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.projects.models.category import Category

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']

admin_site.register(Category, CategoryAdmin)
