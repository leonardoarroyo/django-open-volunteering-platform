import os
import mock
from django.test import TestCase
from django.test.utils import override_settings
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from ovp.apps.salesforce.tasks import push_organization
from ovp.apps.salesforce.tasks import create_client
from ovp.apps.salesforce.tasks import get_organization_id

@override_settings(
    SALESFORCE_INTEGRATION={
        "default": {
            "enabled": os.getenv('DEFAULT_SF_ENABLED', False),
            "username": os.getenv('DEFAULT_SF_USERNAME', None),
            "password": os.getenv('DEFAULT_SF_PASSWORD', None),
            "security_token": os.getenv('DEFAULT_SF_SECURITY_TOKEN', None)
        }
    }
)
class SalesForceTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create(name="test user", email="test@tst.com", password="testpw", object_channel="default")

    def _create_organization(self):
        with mock.patch('ovp.apps.salesforce.tasks.push_organization.apply_async') as mocked:
            return Organization.objects.create(name="blabla", owner=self.owner, object_channel="default")

    def test_signal_triggers_task(self):
        with mock.patch('ovp.apps.salesforce.tasks.push_organization.apply_async') as mocked_task:
            o = Organization.objects.create(name="blabla", owner=self.owner, object_channel="default")
            self.assertFalse(mocked_task.called)
            o.published = True

            def on_commit(func, using=None):
                func()
            with mock.patch('django.db.transaction.on_commit', side_effect=on_commit) as mocked_on_commit:
                o.save()

            self.assertTrue(mocked_task.called)

    @mock.patch('ovp.apps.salesforce.tasks.get_organization_id')
    @mock.patch('ovp.apps.salesforce.tasks.create_organization')
    @mock.patch('ovp.apps.salesforce.tasks.create_contacts')
    def test_task_create_organization(self, mocked_create_contact, mocked_create_organization, mocked_get_organization_id):
        mocked_get_organization_id.return_value = None
        mocked_create_organization.return_value = {"id": "x"}
        organization = self._create_organization()
        push_organization(organization_pk=organization.pk)
        self.assertTrue(mocked_create_organization.called)
        self.assertTrue(mocked_create_contact.called)

    def test_task_update_organization(self):
        organization = self._create_organization()
        push_organization(organization_pk=organization.pk)
        organization.name="test"
        organization.save()
        with mock.patch('ovp.apps.salesforce.tasks.update_organization') as mocked:
            push_organization(organization_pk=organization.pk)
            self.assertTrue(mocked.called)
        push_organization(organization_pk=organization.pk) # Do an actual API request so we can see results online

    def test_check_organization_exists(self):
        organization = self._create_organization()
        push_organization(organization_pk=organization.pk)
        res = get_organization_id(create_client('default'), organization)
        self.assertTrue(len(res) > 0)
