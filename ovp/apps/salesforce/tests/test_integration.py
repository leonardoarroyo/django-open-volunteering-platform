from django.test import TestCase
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization

class IntegrationTest(TestCase):
    def test_str_return_uuid(self):
        owner = User.objects.create(name="test user", email="test@tst.com", password="testpw", object_channel="default")
        o = Organization.objects.create(name="blabla", owner=owner, object_channel="default")
        self.assertTrue(True)
