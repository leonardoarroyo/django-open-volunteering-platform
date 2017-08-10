from django.test import TestCase

from django.db.utils import IntegrityError

from ovp.apps.users.models import User

from ovp.apps.channels.models import Channel

class UserChannelsTestCase(TestCase):
  def setUp(self):
    Channel.objects.create(name="Test channel", slug="test-channel")

  def test_users_with_same_email_on_different_channels(self):
    """ Test users can be created with the same email but on different channels """
    user1 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["default"])
    user2 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["test-channel"])
    self.assertEqual(User.objects.count(), 2)

    with self.assertRaises(IntegrityError) as raised:
      user3 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["default"])
    self.assertEqual(IntegrityError, type(raised.exception))
