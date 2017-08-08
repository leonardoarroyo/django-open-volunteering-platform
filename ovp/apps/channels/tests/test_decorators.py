from django.test import TestCase
from django.test.client import RequestFactory

from ovp.apps.users.models import User

from ovp.apps.channels.models import Channel
from ovp.apps.channels.middlewares.channel import ChannelMiddleware
from ovp.apps.channels.tests.helpers.views import ChannelUserTestViewSet


class ChannelViewsetDecoratorTestCase(TestCase):
  """ Test channel decorator restricts querysets per channel.

  We test the decorator through the viewset.
  """
  def setUp(self):
    # Set up channels
    channel1 = Channel(name="Channel One", slug="channel1")
    channel1.save()

    # Set up test users
    user1 = User(email="test@default.com", password="abc")
    user1.save()

    user2 = User(email="test@channel1.com", password="abc")
    user2.save()
    user2.channels.clear()
    user2.channels.add(channel1)

    user3 = User(email="test@default+channel1.com", password="abc")
    user3.save()
    user3.channels.add(channel1)

    # Set up test view
    self.factory = RequestFactory()
    self.cm = ChannelMiddleware(ChannelUserTestViewSet.as_view({'get': 'list'})) # We also pass it through the middleware

  def test_channels_restriction(self):
    self.request = self.factory.get("/test/")
    response = self.cm(self.request)
    self.assertEqual(response.data["count"], 2)

    self.request = self.factory.get("/test/")
    self.request.META["HTTP_X_OVP_CHANNELS"] = "channel1"
    response = self.cm(self.request)
    self.assertEqual(response.data["count"], 2)

    self.request = self.factory.get("/test/")
    self.request.META["HTTP_X_OVP_CHANNELS"] = "default;channel1"
    response = self.cm(self.request)
    self.assertEqual(response.data["count"], 3)
