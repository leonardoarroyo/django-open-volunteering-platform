from django.contrib import admin
from django import forms

from ovp.apps.channels.admin import admin_site
from ovp.apps.faq.models import Faq

class FaqAdmin(admin.ModelAdmin):
	list_display = ['id', 'question']
	fields = ['category', 'question', 'answer']
	search_fields = [
    'question'
  ]

admin_site.register(Faq, FaqAdmin)
