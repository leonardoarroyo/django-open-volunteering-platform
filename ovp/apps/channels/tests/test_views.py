from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.channels.models import Channel

from ovp.apps.projects.models import Project

from ovp.apps.organizations.models import Organization

from ovp.apps.users.models import User

class MultiChannelViewsetTestCase(TestCase):
  """
  This test uses the Project model and a helper Project viewset
  to test CreateModelWithChannelMixin, but should be applicable
  to any viewset that extends from it.
  """
  def setUp(self):
    self.user = User.objects.create(email="sample_user@gmail.com", password="sample_user")
    self.organization = Organization.objects.create(name="sample organization", owner=self.user)
    self.data = {"name": "Valid Name", "details": "test details", "address": {"typed_address": "r. tecainda, 81, sao paulo"}, "disponibility": {"type": "work", "work": {"description": "abc"}}, "owner": self.user.pk, "organization": self.organization.pk}

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    Channel(name="Test", slug="test-channel").save()

  def test_requests_create_objects_on_default_channel(self):
    """ Assert object defaults to default channel if no header is supplied """
    response = self.client.post(reverse("test-projects-list"), self.data, format="json")

    project = Project.objects.last()
    self.assertTrue(project.channels.count() == 1)
    self.assertTrue(project.channels.first().slug == "default")

  def test_requests_create_objects_on_correct_channel(self):
    """ Assert object are created on the correct channel if header is supplied """
    response = self.client.post(reverse("test-projects-list"), self.data, format="json", HTTP_X_OVP_CHANNELS="test-channel")
    project = Project.objects.last()
    self.assertTrue(project.channels.count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    response = self.client.post(reverse("test-projects-list"), self.data, format="json", HTTP_X_OVP_CHANNELS="default;test-channel")
    project = Project.objects.last()
    self.assertTrue(project.channels.count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")


class SingleChannelViewsetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    Channel(name="Test", slug="test-channel").save()

  def test_requests_create_objects_on_default_channel(self):
    """ Assert object defaults to default channel if no header is supplied """
    data = {"name": "Valid Name", "email": "test@email.com", "password": "123456789abcdefg"}
    response = self.client.post(reverse("test-users-list"), data, format="json")

    user = User.objects.first()
    self.assertTrue(user.channel.slug == "default")

  def test_requests_create_objects_on_correct_channel(self):
    """ Assert object are created on the correct channel if header is supplied """
    data = {"name": "Valid Name", "email": "test@email.com", "password": "123456789abcdefg"}
    response = self.client.post(reverse("test-users-list"), data, format="json", HTTP_X_OVP_CHANNELS="test-channel")

    user = User.objects.first()
    self.assertTrue(user.channel.slug == "test-channel")

  def test_errors_on_multiple_channels(self):
    """ Assert error is raised in case multiple channels are passed to single-channel resource """
    data = {"name": "Valid Name", "email": "test@email.com", "password": "123456789abcdefg"}
    response = self.client.post(reverse("test-users-list"), data, format="json", HTTP_X_OVP_CHANNELS="test-channel;default")

    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data == {"detail": "This is a single channel resource. You must specify only one channel in your request."})
