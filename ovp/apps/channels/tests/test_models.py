from django.test import TestCase
from ovp.apps.channels.models import Channel
from ovp.apps.projects.models import Project
from ovp.apps.users.models import User

class ChannelTestCase(TestCase):
  def setUp(self):
    self.user = User(email="test@user.com", password="test_password")
    self.user.save()

  def test_migrations_create_default_channel(self):
    self.assertTrue(Channel.objects.count() == 1)
    self.assertTrue(Channel.objects.first().name == "default")

  def test_models_that_extend_channel_relationship_default_channel_on_save(self):
    """ Assert models that extend ChannelRelationship model automatically get associated with default channel on save method """
    project = Project(name="test", owner=self.user)
    project.save()

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "default")

  def test_models_that_extend_channel_relationship_can_be_created_with_custom_channels_on_save(self):
    """ Assert models that extend ChannelRelationship can be created with custom channels on save method """
    Channel(name="Test", slug="test-channel").save()

    project = Project(name="test", owner=self.user)
    project.save(object_channels=["test-channel"])

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    project = Project(name="test", owner=self.user)
    project.save(object_channels=["default", "test-channel"])

    self.assertTrue(project.channels.all().count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")

  def test_models_that_extend_channel_relationship_default_channel_on_create(self):
    """ Assert models that extend ChannelRelationship model automatically get associated with default channel on manager create method """
    project = Project.objects.create(name="test", owner=self.user)

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "default")

  def test_models_that_extend_channel_relationship_can_be_created_with_custom_channels_on_create(self):
    """ Assert models that extend ChannelRelationship can be created with custom channels on manager create method """
    Channel(name="Test", slug="test-channel").save()

    project = Project.objects.create(name="test", owner=self.user, object_channels=["test-channel"])

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    project = Project.objects.create(name="test", owner=self.user, object_channels=["default", "test-channel"])

    self.assertTrue(project.channels.all().count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")

