from django.conf import settings
import importlib

def get_settings(string="OVP_FAQ"):
  return getattr(settings, string, {})
