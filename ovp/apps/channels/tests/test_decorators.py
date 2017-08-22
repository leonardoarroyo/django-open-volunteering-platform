from mock import Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from ovp.apps.users.models import User

from ovp.apps.projects.models.project import Project

from ovp.apps.channels.models import Channel
from ovp.apps.channels.tests.helpers.views import ChannelProjectTestViewSet
from ovp.apps.channels.middlewares.channel import ChannelMiddleware


class ChannelViewsetDecoratorTestCase(TestCase):
  """ Test channel decorator restricts querysets per channel.

  We test the decorator through the viewset.
  """
  def setUp(self):
    # Set up channels
    channel1 = Channel(name="Channel One", slug="channel1")
    channel1.save()

    # Set up test projects
    user = User.objects.create(email="test@default.com", password="abc", object_channels=["default"])

    project1 = Project.objects.create(name="test", owner=user, object_channels=["default"])
    project1.save()

    project2 = Project.objects.create(name="test", owner=user, object_channels=["channel1"])
    project2.channels.clear()
    project2.channels.add(channel1)

    project3 = Project.objects.create(name="test", owner=user, object_channels=["default", "channel1"])
    project3.channels.add(channel1)

    # Set up test view
    self.factory = RequestFactory()
    self.cm = ChannelMiddleware(ChannelProjectTestViewSet.as_view({'get': 'list'})) # We also pass it through the middleware

  def _generate_request(self):
    request = self.factory.get("/test/")
    request.user = AnonymousUser()
    request.session = {}
    return request

  def test_channels_restriction(self):
    request = self._generate_request()
    response = self.cm(request)
    self.assertEqual(response.data["count"], 2)

    request = self._generate_request()
    request.META["HTTP_X_OVP_CHANNELS"] = "channel1"
    response = self.cm(request)
    self.assertEqual(response.data["count"], 2)

    request = self._generate_request()
    request.META["HTTP_X_OVP_CHANNELS"] = "default;channel1"
    response = self.cm(request)
    self.assertEqual(response.data["count"], 3)
