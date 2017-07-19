from django.test import TestCase
from django.test.utils import override_settings

from ovp.apps.core.helpers import get_address_model
from ovp.apps.core.models import SimpleAddress, GoogleAddress

class GetAddressModelHelperTestCase(TestCase):
  def test_default_model(self):
    """Assert GoogleAddress is the default address model"""
    model = get_address_model()
    self.assertTrue(model == GoogleAddress)

  @override_settings(OVP_CORE={'ADDRESS_MODEL': 'ovp.apps.core.models.SimpleAddress'})
  def test_setting(self):
    """Assert it's possible to modify the model by changing the setting"""
    model = get_address_model()
    self.assertTrue(model == SimpleAddress)
