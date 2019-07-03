from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.gallery.models import Gallery

from martor.widgets import AdminMartorWidget


class GalleryAdmin(ChannelModelAdmin):
  fields = ['id', 'uuid', 'name',  'description', 'owner', 'images', ('created_date', 'modified_date')]

  list_display = ['id', 'uuid', 'name']

  list_filter = []

  list_editable = []

  search_fields = ['id', 'content']

  readonly_fields = ['id', 'uuid', 'created_date', 'modified_date']

  raw_id_fields = []

  formfield_overrides = {
    models.TextField: {'widget': AdminMartorWidget},
  }

  def post(self, obj):
    return obj.__str__()


admin_site.register(Gallery, GalleryAdmin)
