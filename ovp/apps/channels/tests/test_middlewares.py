from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock
from ovp.apps.channels.middlewares.channel import ChannelMiddleware
from ovp.apps.core.views import startup

class ChannelMiddlewareTestCase(TestCase):
  def setUp(self):
    self.cm = ChannelMiddleware(startup)
    self.factory = RequestFactory()
    self.request = self.factory.get("/startup/")
    self.request.user = Mock()

  def test_default_channel_if_no_header_is_supplied(self):
    """ Assert requests defaults to default channel if no header is supplied """
    request = self.cm._add_channels(self.request)
    self.assertTrue(request.channels == ["default"])

  def test_default_channels_included_in_response_header_no_channel_supplied(self):
    """ Assert response returns channel even without request header """
    response = self.cm(self.request)
    self.assertTrue(response["X-OVP-Channels"] == "default")

  def test_request_has_correct_channels_if_header_is_supplied(self):
    """ Assert requests recognizes correct channels if header is supplied """
    self.request.META["HTTP_X_OVP_CHANNELS"] = "test-channel-1 ; test-channel-2;  last-channel "
    request = self.cm._add_channels(self.request)
    self.assertTrue(request.channels == ["test-channel-1", "test-channel-2", "last-channel"])

  def test_correct_channels_included_in_response_header_if_channel_supplied(self):
    """ Assert response returns channels if channel is supplied on request """
    self.request.META["HTTP_X_OVP_CHANNELS"] = "test-channel-1 ; test-channel-2;  last-channel "
    response = self.cm(self.request)
    self.assertTrue(response["X-OVP-Channels"] == "test-channel-1;test-channel-2;last-channel")
