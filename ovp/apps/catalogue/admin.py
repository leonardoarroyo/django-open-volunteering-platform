from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import CompactInline

from ovp.apps.catalogue.models import Catalogue
from ovp.apps.catalogue.models import Section
from ovp.apps.catalogue.models import SectionFilter


class SectionInline(CompactInline):
  model = Section
  fields = ["name", "slug"]
  show_change_link = True

class SectionFilterInline(CompactInline):
  model = SectionFilter
  fields = ["section", "type"]
  show_change_link = True

class CatalogueAdmin(ChannelModelAdmin):
  fields = ["name", "slug"]
  list_display = ["name", "slug"]
  search_fields = ["id", "name", "slug"]
  inlines = [SectionInline]

class SectionAdmin(ChannelModelAdmin):
  fields = ["name", "slug", "catalogue"]
  list_display = ["name", "slug", "catalogue"]
  search_fields = ["id", "name", "slug", "catalogue__name", "catalogue__slug"]
  inlines = [SectionFilterInline]

class SectionFilterAdmin(ChannelModelAdmin):
  fields = ["section", "type"]
  list_display = ["section", "type"]
  search_fields = []


admin_site.register(Catalogue, CatalogueAdmin)
admin_site.register(Section, SectionAdmin)
