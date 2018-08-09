from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.template.defaultfilters import slugify
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

def generate_slug(channel, model, name):
  if name:
    slug = slugify(name)[0:99]
    append = ''
    i = 0

    query = model.objects.filter(slug=slug + append, channel__slug=channel)
    while query.count() > 0:
      i += 1
      append = '-' + str(i)
      query = model.objects.filter(slug=slug + append, channel__slug=channel)
    return slug + append
  return None

def get_address_model():
  """ Returns application address model

  The address model can be modified by setting OVP_CORE.ADDRESS_MODEL.

  Returns:
    class: Address model class

    The default model returned is ovp_core.models.GoogleAddress

  """
  model_name = get_settings().get("ADDRESS_MODEL", "ovp.apps.core.models.GoogleAddress")
  return import_from_string(model_name)


def get_address_serializers():
  """ Return application address serializer tuple

  The tuple can be modified by setting OVP_CORE.ADDRESS_SERIALIZER_TUPLE.

  Returns:
    tuple: A tuple with 3 serializers

    The default tuple returned is (GoogleAddressSerializer, GoogleAddressLatLngSerializer, GoogleAddressCityStateSerializer).
    The first one is the default serializer, usually used to create and update addresses.
    The second extends the first one but also includes 'lat' and 'lng' field, used to create pins on maps.
    The third is a simplified serializer containing only field 'city_state'. This is used on search.

  """
  serializers = get_settings().get('ADDRESS_SERIALIZER_TUPLE', ('ovp.apps.core.serializers.GoogleAddressSerializer', 'ovp.apps.core.serializers.GoogleAddressLatLngSerializer', 'ovp.apps.core.serializers.GoogleAddressCityStateSerializer', 'ovp.apps.core.serializers.GoogleAddressShortSerializer'))
  return [import_from_string(s) for s in serializers]
