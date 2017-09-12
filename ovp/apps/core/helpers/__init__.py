from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
import importlib

from ovp.apps.channels.cache import get_channel_setting

def get_settings(string="OVP_CORE"):
  return getattr(settings, string, {})


def import_from_string(val):
  try:
    # Nod to tastypie's use of importlib.
    parts = val.split('.')
    module_path, class_name = '.'.join(parts[:-1]), parts[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
  except ImportError as e:
    msg = "Could not import '%s' for setting. %s: %s." % (val, e.__class__.__name__, e)
    raise ImportError(msg)


def is_email_enabled(channel, email):
  """ Emails are activated by default.
      Create a template named {email}-disable.txt to disable it.
  """
  disabled_emails = get_channel_setting(channel, "DISABLE_EMAIL")

  if email in disabled_emails:
    return False

  return True


def get_email_subject(channel, email, default):
  """ Allows for email subject overriding """
  try:
    title = get_template('{}/email/{}-subject.txt'.format(channel, email)).render().replace("\n", "")
  except TemplateDoesNotExist as e:
    title = default

  return _(title)
