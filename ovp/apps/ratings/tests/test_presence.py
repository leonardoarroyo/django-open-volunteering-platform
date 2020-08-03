import json
from django.test import TestCase
from django.core.cache import cache

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.channels.models import ChannelSetting
from ovp.apps.users.models import User
from ovp.apps.projects.models import Project, Apply
from ovp.apps.organizations.models import Organization
from ovp.apps.ratings.models import RatingRequest
from ovp.apps.ratings.models import RatingParameter
from ovp.apps.ratings.models import Rating



class RatingViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="a",
            email="testmail@test.com",
            password="test_returned",
            object_channel="default")
        self.user2 = User.objects.create_user(
            name="b",
            email="testmail2@test.com",
            password="test_returned",
            object_channel="default")
        self.organization = Organization.objects.create(
            name="test org", owner=self.user, object_channel="default")
        self.project = Project.objects.create(
            name="test project",
            slug="test-slug",
            details="abc",
            description="abc",
            owner=self.user,
            organization=self.organization,
            published=False,
            object_channel="default")
        Apply.objects.create(user=self.user, project=self.project, object_channel="default")

        rp1 = RatingParameter.objects.create(
            slug="user-participated", type=3, object_channel="default")
        rp2 = RatingParameter.objects.create(
            slug="user-opinion", type=1, object_channel="default")
        rp3 = RatingParameter.objects.create(
            slug="user-project-rating", type=2, object_channel="default")

        cache.clear()

    def test_closing_project_creates_rating_request(self):
        ChannelSetting.objects.create(key="ENABLE_USER_PRESENCE_RATING_REQUEST", value="1", object_channel="default")
        self.assertEqual(RatingRequest.objects.count(), 0)
        self.project.closed = True
        self.project.save()
        self.assertEqual(RatingRequest.objects.count(), 1)
        self.assertEqual(RatingRequest.objects.last().rating_parameters.count(), 3)

    def test_closing_project_doesnt_create_request_if_not_enabled(self):
        self.assertEqual(RatingRequest.objects.count(), 0)
        self.project.closed = True
        self.project.save()
        self.assertEqual(RatingRequest.objects.count(), 0)
