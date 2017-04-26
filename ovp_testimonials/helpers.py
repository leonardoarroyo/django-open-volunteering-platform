from django.conf import settings
from haystack import connection_router, connections
from haystack.inputs import Raw

def get_settings(string="OVP_TESTIMONIALS"):
  return getattr(settings, string, {})
