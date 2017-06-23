from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
  fields = [
    ('id', 'rating'),
    ('user'),
    ('published', 'created_date'),
    'content',
    'video_url',
    ('image', 'image_tag'),
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

  readonly_fields = ['id', 'created_date', 'video_url', 'image_tag']
  raw_id_fields = []

  def video_url(self, obj):
    if obj.video:
      return '<a href="https://www.youtube.com/watch?v={}" target="_blank">Link do Vídeo</a>'.format(obj.video)
  video_url.short_description = 'Vídeo'
  video_url.allow_tags = True

  def image_tag(self, obj):
    if obj.image.image_medium is not None:
      return '<img style="max-width: 100%" src="{}" />'.format(obj.image.image_medium)
  image_tag.short_description = 'Imagem'
  image_tag.allow_tags = True


admin.site.register(Testimonial, TestimonialAdmin)
admin.site._registry[Testimonial].display_on_main_menu = True
