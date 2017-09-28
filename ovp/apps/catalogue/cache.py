from django.core.cache import cache
from ovp.apps.catalogue.models import Catalogue
from ovp.apps.channels.defaults import DEFAULT_SETTINGS

from collections import OrderedDict

def get_catalogue(channel, slug):
  key = "catalogue-{}-{}".format(channel, slug)
  cache_ttl = 60
  result = cache.get(key)

  if not result:
    try:
      catalogue = Catalogue.objects.prefetch_related("sections", "sections__filters").get(slug=slug, channel__name=channel)
    except Catalogue.DoesNotExist:
      result = None
    else:
      result = {
        "name": catalogue.name,
        "slug": catalogue.slug,
        "sections": [],
      }

      for section in catalogue.sections.all():
        section_dict = {
          "name": section.name,
          "slug": section.slug,
          "filters": []
        }
        for section_filter in section.filters.all():
          section_dict["filters"] = section_filter.filter.get_filter_kwargs()

        result["sections"].append(section_dict)

    cache.set(key, result, cache_ttl)

  return result
