import os

from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from ovp.apps.donations.models import Transaction
from ovp.apps.donations.backends.zoop import ZoopBackend
from ovp.apps.donations.tests.helpers import card_token


class TestDonationsViewSet(TestCase):
  def setUp(self):
    self.backend = ZoopBackend()
    self.client = APIClient()
    self.user = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="default")
    self.donator = User.objects.create_user(name="a", email="donator@test.com", password="test_returned", object_channel="default")
    self.organization = Organization.objects.create(name="test org", owner=self.user, object_channel="default", allow_donations=True)

    self.data = {
      "organization_id": self.organization.id,
      "amount": 100,
      "token": "invalid"
    }

  def test_cant_donate_unauthenticated(self):
    response = self.client.post(reverse("donation-donate"), format="json")
    self.assertEqual(response.status_code, 401)

  def test_cant_donate_if_organization_not_flagged(self):
    self.organization.allow_donations = False
    self.organization.save()
    self.client.force_authenticate(user=self.donator)

    response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'organization_id': ["Organization with 'id' 1 and 'allow_donations' True does not exist."]})

  def test_can_donate(self):
    self.client.force_authenticate(user=self.donator)
    self.data["token"] = card_token("5201561050024014")

    self.assertEqual(Transaction.objects.all().count(), 0)

    response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data, {'status': 'succeeded', 'message': 'Transaction was authorized.'})

    self.assertEqual(Transaction.objects.all().count(), 1)
    transaction = Transaction.objects.last()
    self.assertEqual(transaction.user, self.donator)
    self.assertEqual(transaction.organization, self.organization)
    self.assertEqual(transaction.amount, self.data["amount"])
    self.assertEqual(transaction.status, "succeeded")
    self.assertEqual(transaction.message, "Transaction was authorized.")
    self.assertEqual(transaction.used_token, self.data["token"])
    self.assertTrue(transaction.backend_transaction_id)
    self.assertTrue(transaction.backend_transaction_number)

  def test_cant_donate_invalid_card(self):
    self.client.force_authenticate(user=self.donator)

    self.data["token"] = card_token("6011457819940087")
    response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
    self.assertEqual(response.status_code, 402)
    self.assertEqual(response.data, {"status": "failed", "message": "Your card was declined. For information about why your credit card was declined or rejected, please contact your bank or credit card vendor.", "category": "card_declined"})

    self.data["token"] = card_token("4929710426637678")
    response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
    self.assertEqual(response.status_code, 402)
    self.assertEqual(response.data, {"status": "failed", "message": "Your card was declined. For information about why your credit card was declined or rejected, please contact your bank or credit card vendor.", "category": "card_declined"})

  def test_cant_donate_timeout(self):
    self.client.force_authenticate(user=self.donator)

    self.data["token"] = card_token("4710426743216178")
    response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
    self.assertEqual(response.status_code, 408)
    self.assertEqual(response.data, {"status": "timeout", "message": "Credit card process is temporarily unavailable at the specified location. Please try again later. If the problem persists, please contact Technical Support (support@pagzoop.com).", "category": "service_request_timeout"})

  # Zoop broken for this operation
  #def test_cant_donate_card_declined(self):
  #  self.client.force_authenticate(user=self.donator)
  #
  #  self.data["token"] = card_token("4556629972668582")
  #  response = self.client.post(reverse("donation-donate"), data=self.data, format="json")
  #  self.assertEqual(response.status_code, 402)
  #  self.assertEqual(response.data, {"status": "failed", "message": "xxxxx", "category": "card_declined"})