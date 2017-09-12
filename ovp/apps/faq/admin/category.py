from django.contrib import admin
from django import forms

from ovp.apps.faq.models import FaqCategory

class FaqCategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


admin.site.register(FaqCategory, FaqCategoryAdmin)
