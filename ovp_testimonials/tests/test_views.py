from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from django.core.cache import cache

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users.models import User
from ovp_users.models.profile import get_profile_model
from ovp_projects.models import Project, Job
from ovp_organizations.models import Organization
from ovp_core.models import GoogleAddress, Cause, Skill

import json



"""
Helpers
"""
def create_sample_users():
  user1 = User(name="user one", email="testmail1@test.com", password="test_returned")
  user1.save()

  UserProfile = get_profile_model()
  profile1 = UserProfile(user=user1, full_name="user one", about="about one")
  profile1.save()

"""
Tests
"""
class TestimonialTestCase(TestCase):
  def setUp(self):
    pass
