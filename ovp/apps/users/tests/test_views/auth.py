from django.test import TestCase

from ovp.apps.users.models import User

from ovp.apps.channels.models import Channel

from ovp.apps.users.tests.helpers import authenticate
from ovp.apps.users.tests.helpers import create_user
from ovp.apps.users.tests.helpers import create_token

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class JWTAuthTestCase(TestCase):
  def test_can_login(self):
    """ Assert that it's possible to login """
    user = create_user('test_can_login@test.com', 'validpassword')
    response = authenticate()
    self.assertTrue(response.data['token'] != None)

  def test_cant_login_wrong_password(self):
    """ Assert that it's not possible to login with wrong password """
    user = create_user('test_can_login@test.com', 'invalidpassword')
    response = authenticate()
    self.assertTrue(response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.')

  def test_can_login_two_users_same_email(self):
    """ Assert that it's possible to login if two users have the same email on different channels.

        JWT would by default raise an exception because it tries to .get the user and it returns multiple results.
        Note that a JWT token refers to user and password, therefore it is possible to authenticate to multiple channels
        if a single token if the user email and password is the same.
    """
    Channel.objects.create(name="Test", slug="test-channel")
    user1 = User.objects.create(email="test_can_login@test.com", password="validpassword", object_channel="default")
    user2 = User.objects.create(email="test_can_login@test.com", password="validpassword", object_channel="test-channel")
    response = authenticate()
    token = response.data['token']

    response = APIClient().get(reverse('user-current-user'), format="json", HTTP_AUTHORIZATION="JWT {}".format(token))
    self.assertEqual(response.data["uuid"], str(user1.uuid))
    response = APIClient().get(reverse('user-current-user'), format="json", HTTP_AUTHORIZATION="JWT {}".format(token), HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(response.data["uuid"], str(user2.uuid))
