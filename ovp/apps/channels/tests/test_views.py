from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.channels.models import Channel
from ovp.apps.users.models import User

class ChannelViewsTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    Channel(name="Test", slug="test-channel").save()

  def test_requests_create_objects_on_default_channel(self):
    """ Assert object defaults to default channel if no header is supplied """
    data = {"name": "Valid Name", "email": "test@email.com", "password": "123456789abcdefg"}
    response = self.client.post(reverse("test-users-list"), data, format="json")

    user = User.objects.first()
    self.assertTrue(user.channels.count() == 1)
    self.assertTrue(user.channels.first().slug == "default")

  def test_requests_create_objects_on_correct_channel(self):
    """ Assert object are created on the correct channel if header is supplied """
    data = {"name": "Valid Name", "email": "test@email.com", "password": "123456789abcdefg"}
    response = self.client.post(reverse("test-users-list"), data, format="json", HTTP_X_OVP_CHANNELS="test-channel")

    user = User.objects.first()
    self.assertTrue(user.channels.count() == 1)
    self.assertTrue(user.channels.first().slug == "test-channel")
