from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.projects.models.category import Category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']

admin.site.register(Category, CategoryAdmin)