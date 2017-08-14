from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.users.models import User

from ovp.apps.channels.models import Channel

class UserChannelsTestCase(TestCase):
  def setUp(self):
    Channel.objects.create(name="Test channel", slug="test-channel")
    self.client = APIClient()

    self.user1 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["default"])
    self.user2 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["test-channel"])

  def test_users_with_same_email_on_different_channels(self):
    """ Test users can be created with the same email but on different channels """
    self.assertEqual(User.objects.count(), 2)

    with self.assertRaises(IntegrityError) as raised:
      user3 = User.objects.create(email="sample_user@gmail.com", password="sample_user", object_channels=["default"])
    self.assertEqual(IntegrityError, type(raised.exception))


  def test_user_channel_based_auth_backend(self):
    """ Test user authentication on different channels """
    user1 = authenticate(email="sample_user@gmail.com", password="sample_user", channel="default")
    user2 = authenticate(email="sample_user@gmail.com", password="sample_user", channel="test-channel")

    self.assertEqual(user1, self.user1)
    self.assertEqual(user2, self.user2)
    self.assertTrue(user1 != None)
    self.assertTrue(user2 != None)


  def test_user_channel_based_auth_view(self):
    """ Test user authentication on different channels """
    # Authenticate user one
    response = self.client.post(reverse("api-token-auth"), {"email": "sample_user@gmail.com", "password": "sample_user"}, format="json", HTTP_X_OVP_CHANNELS="default")
    self.assertTrue(response.status_code == 200)
    self.assertTrue("token" in response.data)

    # Authenticate user two
    response = self.client.post(reverse("api-token-auth"), {"email": "sample_user@gmail.com", "password": "sample_user"}, format="json", HTTP_X_OVP_CHANNELS="test-channel")
    self.assertTrue(response.status_code == 200)
    self.assertTrue("token" in response.data)

    # Multiple channel authentication
    response = self.client.post(reverse("api-token-auth"), {"email": "sample_user@gmail.com", "password": "sample_user"}, format="json", HTTP_X_OVP_CHANNELS="default;test-channel")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data == {'detail': 'This is a single channel resource. You must specify only one channel in your request.'})

    # Wrong channel authentication
    response = self.client.post(reverse("api-token-auth"), {"email": "sample_user@gmail.com", "password": "sample_user"}, format="json", HTTP_X_OVP_CHANNELS="wrong-channel")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data == {'non_field_errors': ['Unable to log in with provided credentials.']})
