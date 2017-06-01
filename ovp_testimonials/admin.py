from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
  fields = [
    ('id', 'rating'),
    ('user'),
    ('published', 'created_date'),
    'content'
    ]

  list_display = [
    'id', 'user', 'rating', 'published', 'created_date'
    ]

  list_filter = [
    'published', 'rating'
    ]

  list_editable = ['published']

  search_fields = [
    'user__name', 'content'
    ]

  readonly_fields = ['id', 'created_date']
  raw_id_fields = []


admin.site.register(Testimonial, TestimonialAdmin)
admin.site._registry[Testimonial].display_on_main_menu = True
