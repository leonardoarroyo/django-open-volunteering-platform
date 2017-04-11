from django.contrib import admin
from django import forms

from ovp_faq.models import Faq

class FaqAdmin(admin.ModelAdmin):
	list_display = ['id', 'question']
	fields = ['question', 'answer', 'category']


admin.site.register(Faq, FaqAdmin)