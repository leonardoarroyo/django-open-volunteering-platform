from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import CompactInline

from ovp.apps.catalogue.models import Catalogue
from ovp.apps.catalogue.models import Section
from ovp.apps.catalogue.models import SectionFilter

from ovp.apps.catalogue.models import CategoryFilter


##################################
# Mixins                         #
##################################
class FilterObjectMixin():
  def filter_object(self, obj):
    if obj.filter:
      url = reverse('admin:%s_%s_change' %(obj.filter._meta.app_label,  obj.filter._meta.model_name),  args=[obj.filter.id])
      return '<a href="%s">Edit</a>' % url
    else:
      return _('No filter')
  filter_object.allow_tags = True

  def filter_information(self, obj):
    if obj.filter:
      return obj.filter.filter_information().replace("\n", "<br>")
    return _('No filter')
  filter_information.allow_tags = True


##################################
# Inlines                        #
##################################
class SectionInline(CompactInline):
  model = Section
  fields = ["name", "slug"]
  show_change_link = True

class SectionFilterInline(FilterObjectMixin, CompactInline):
  model = SectionFilter
  fields = ["section", "type", "filter_object", "filter_information"]
  readonly_fields = ["filter_object", "filter_information"]
  show_change_link = True


##################################
# Admin                          #
##################################
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

class SectionFilterAdmin(FilterObjectMixin, ChannelModelAdmin):
  fields = ["section", "type", "filter_object", "filter_information"]
  list_display = ["section", "type"]
  readonly_fields = ["filter_object", "filter_information"]
  search_fields = []


admin_site.register(Catalogue, CatalogueAdmin)
admin_site.register(Section, SectionAdmin)
admin_site.register(SectionFilter, SectionFilterAdmin)


##################################
# Filters admin                  #
##################################
class CategoryFilterAdmin(ChannelModelAdmin):
  fields = ["categories"]
  list_display = []
  search_fields = []

admin_site.register(CategoryFilter, CategoryFilterAdmin)
