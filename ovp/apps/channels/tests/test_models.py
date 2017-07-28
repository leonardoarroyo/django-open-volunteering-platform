from django.test import TestCase
from ovp.apps.channels.models import Channel
from ovp.apps.projects.models import Project
from ovp.apps.users.models import User

class ChannelTestCase(TestCase):
  def test_migrations_create_default_channel(self):
    self.assertTrue(Channel.objects.count() == 1)
    self.assertTrue(Channel.objects.first().name == "default")

  def test_models_that_extend_channel_relationship(self):
    """ Assert models that extend ChannelRelationship model automatically get associated with default channel """
    user = User(email="test@user.com", password="test_password")
    user.save()

    project = Project(name="test", owner=user)
    project.save()

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().name == "default")
