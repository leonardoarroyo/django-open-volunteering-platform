from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock
from ovp.apps.channels.middlewares.channel import ChannelMiddleware
from ovp.apps.channels.models.channel import Channel
from ovp.apps.core.views import startup

class ChannelMiddlewareTestCase(TestCase):
  def setUp(self):
    Channel.objects.create(name="Test channel", slug="test-channel-1")
    self.cm = ChannelMiddleware(startup)
    self.factory = RequestFactory()
    self.request = self.factory.get("/startup/")
    self.request.user = Mock()
    self.request.session = {}

  def test_default_channel_if_no_header_is_supplied(self):
    """ Assert requests defaults to default channel if no header is supplied """
    request = self.cm._add_channel(self.request)
    self.assertTrue(request.channel == "default")

  def test_default_channel_included_in_response_header_no_channel_supplied(self):
    """ Assert response returns channel even without request header """
    response = self.cm(self.request)
    self.assertTrue(response["X-OVP-Channel"] == "default")

  def test_request_has_correct_channel_if_header_is_supplied(self):
    """ Assert requests recognizes correct channel if header is supplied """
    self.request.META["HTTP_X_OVP_CHANNEL"] = "test-channel-1"
    request = self.cm._add_channel(self.request)
    self.assertTrue(request.channel == "test-channel-1")

  def test_correct_channel_included_in_response_header_if_channel_supplied(self):
    """ Assert response returns channel if channel is supplied on request """
    self.request.META["HTTP_X_OVP_CHANNEL"] = "test-channel-1"
    response = self.cm(self.request)
    self.assertTrue(response["X-OVP-Channel"] == "test-channel-1")

  def test_correct_response_when_incorrect_channel(self):
    """ Assert response is correct if incorrect channel is supplied """
    self.request.META["HTTP_X_OVP_CHANNEL"] = "invalid"
    response = self.cm(self.request)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.content, b'{"detail": "Invalid channel."}')
