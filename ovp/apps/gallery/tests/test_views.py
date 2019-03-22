import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from ovp.apps.gallery.models import Gallery
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import json

User = get_user_model()

class GalleryViewSetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user1 = User.objects.create(email="test1@gmail.com", password="test1", object_channel="default")
    self.user2 = User.objects.create(email="test2@gmail.com", password="test1", object_channel="default")

  def test_can_create_gallery(self):
    data = {"name": "test", "description": "abc123"}
    response = self.client.post(reverse("gallery-list"), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 401)

    self.client.force_authenticate(user=self.user1)
    response = self.client.post(reverse("gallery-list"), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 201)
    self.assertTrue("uuid" in response.data)
    self.assertEqual(response.data["name"], "test")
    self.assertEqual(response.data["description"], "abc123")
    self.assertEqual(Gallery.objects.last().owner, self.user1)

  def test_can_edit_gallery(self):
    data = {"name": "test2", "description": "edited"}
    self.test_can_create_gallery()
    uuid_str = str(Gallery.objects.last().uuid)
    response = self.client.patch(reverse("gallery-detail", [uuid_str]), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["name"], "test2")
    self.assertEqual(response.data["description"], "edited")

    self.client = APIClient()
    response = self.client.patch(reverse("gallery-detail", [uuid_str]), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 401)

    self.client.force_authenticate(user=self.user2)
    response = self.client.patch(reverse("gallery-detail", [uuid_str]), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 403)

  def test_can_delete_gallery(self):
    self.test_can_create_gallery()
    uuid_str = str(Gallery.objects.last().uuid)
    response = self.client.delete(reverse("gallery-detail", [uuid_str]), format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 200)

  def test_can_associate_gallery(self):
    pass