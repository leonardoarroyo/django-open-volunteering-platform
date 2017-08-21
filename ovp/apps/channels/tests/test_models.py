from django.test import TestCase

from ovp.apps.channels.models import Channel
from ovp.apps.channels.exceptions import UnexpectedMultipleChannelsError
from ovp.apps.channels.exceptions import UnexpectedChannelAssociationError
from ovp.apps.channels.exceptions import NoChannelSupplied

from ovp.apps.projects.models import Project

from ovp.apps.users.models import User

class MultiChannelTestCase(TestCase):
  def setUp(self):
    self.user = User(email="test@user.com", password="test_password")
    self.user.save(object_channels=["default"])

  def test_migrations_create_default_channel(self):
    self.assertTrue(Channel.objects.count() == 2)
    self.assertTrue(Channel.objects.first().name == "null")
    self.assertTrue(Channel.objects.last().name == "default")

  def test_models_that_extend_multi_channel_relationship_raise_errors_if_no_channel_supplied_on_save(self):
    """ Assert models that extend MultiChannelRelationship model raise errors if no object_channels is passed on save method """
    project = Project(name="test", owner=self.user)

    with self.assertRaises(NoChannelSupplied):
      project.save()

    self.assertEqual(Project.objects.count(), 0)

  def test_models_that_extend_multi_channel_relationship_can_be_created_with_custom_channels_on_save(self):
    """ Assert models that extend MultiChannelRelationship can be created with custom channels on save method """
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

  def test_models_that_extend_multi_channel_relationship_raise_errors_if_no_channel_supplied_on_create(self):
    """ Assert models that extend MultiChannelRelationship model raise errors if no object_channels is passed on manager create method """
    with self.assertRaises(NoChannelSupplied):
      project = Project.objects.create(name="test", owner=self.user)

    self.assertEqual(Project.objects.count(), 0)

  def test_models_that_extend_multi_channel_relationship_can_be_created_with_custom_channels_on_create(self):
    """ Assert models that extend MultiChannelRelationship can be created with custom channels on manager create method """
    Channel(name="Test", slug="test-channel").save()

    project = Project.objects.create(name="test", owner=self.user, object_channels=["test-channel"])

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    project = Project.objects.create(name="test", owner=self.user, object_channels=["default", "test-channel"])

    self.assertTrue(project.channels.all().count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")


class SingleChannelTestCase(TestCase):
  def test_models_that_extend_single_channel_relationship_raise_error_if_no_channel_supplied_on_save(self):
    """ Assert models that extend SingleChannelRelationship model raises error if no channel supplied on save method """
    user = User(email="test@user.com", password="test_password")
    with self.assertRaises(NoChannelSupplied):
      user.save()

    self.assertEqual(User.objects.count(), 0)

  def test_models_that_extend_single_channel_relationship_can_be_created_with_custom_channel_on_save(self):
    """ Assert models that extend SingleChannelRelationship can be created with custom channel on save method """
    Channel(name="Test", slug="test-channel").save()
    user = User(email="test@user.com", password="test_password")
    user.save(object_channels=["test-channel"])

    self.assertTrue(user.channel.slug == "test-channel")

  def test_models_that_extend_single_channel_relationship_raise_error_if_no_channel_supplied_on_create(self):
    """ Assert models that extend SingleChannelRelationship model raises error if no channel supplied on manager create method """
    with self.assertRaises(NoChannelSupplied):
      user = User.objects.create(email="test@user.com", password="test_password")

    self.assertEqual(User.objects.count(), 0)

  def test_models_that_extend_single_channel_relationship_can_be_created_with_custom_channel_on_create(self):
    """ Assert models that extend SingleChannelRelationship can be created with custom channel on manager create method """
    Channel(name="Test", slug="test-channel").save()
    user = User.objects.create(email="test@user.com", password="test_password", object_channels=["test-channel"])
    self.assertTrue(user.channel.slug == "test-channel")

  def test_models_that_extend_single_channel_relationship_raise_exception_if_associated_with_multiple_channels(self):
    """ Assert models that extend SingleChannelRelationship raise exception if associated_with_multiple_channels """
    Channel(name="Test", slug="test-channel").save()
    with self.assertRaises(UnexpectedMultipleChannelsError):
      user = User.objects.create(email="test@user.com", password="test_password", object_channels=["default", "test-channel"])

    user = User(email="test@user.com", password="test_password")
    with self.assertRaises(UnexpectedMultipleChannelsError):
      user.save(object_channels=["default", "test-channel"])

  def test_models_that_extend_single_channel_cant_associate_channel_directly(self):
    """ Assert models that extend SingleChannelRelationship raise exception when trying to associate channel directly """
    channel = Channel.objects.create(name="Test", slug="test-channel")
    user = User(email="test@user.com", password="test_password", channel=channel)
    with self.assertRaises(UnexpectedChannelAssociationError):
      user.save()

    with self.assertRaises(UnexpectedChannelAssociationError):
      user = User.objects.create(email="test@user.com", password="test_password", channel=channel)
