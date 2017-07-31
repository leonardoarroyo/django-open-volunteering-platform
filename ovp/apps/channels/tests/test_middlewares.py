from django.test import TestCase
from mock import Mock
from ovp.apps.channels.middlewares.channel import ChannelMiddleware

class ChannelMiddlewareTestCase(TestCase):
  def setUp(self):
    self.cm = ChannelMiddleware()
    self.request = Mock()
    self.request.session = {}

  def test_default_channel_if_no_header_is_supplied(self):
    """ Assert requests defaults to default channel if no header is supplied """
    response = self.cm.process_request(self.request)
