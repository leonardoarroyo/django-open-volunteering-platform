# test filter sent recently
# test filter no content
from django.test import TestCase
from django.test import TransactionTestCase
from django.core import mail
from django.db.models import Value, IntegerField
from ovp.apps.channels.models import Channel
from ovp.apps.digest.digest import generate_content_for_user
from ovp.apps.digest.digest import send_campaign
from ovp.apps.search.tests.test_views import create_sample_projects
from ovp.apps.search.tests.test_views import create_sample_users
from ovp.apps.users.models import User

class DigestTestCase(TestCase):
  def setUp(self):
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_projects()
    create_sample_users()

  def test_num_queries_generate_content(self):
    user = User.objects.annotate(campaign=Value(0, IntegerField())) \
           .select_related('channel', 'users_userprofile_profile') \
           .get(email="testmail1@test.com")

    with self.assertNumQueries(2):
      content = generate_content_for_user(user)

    self.assertEqual(len(content['projects']), 2)

  def test_send_campaign(self):
    users = ["testmail1@test.com"]

    mail.outbox = []
    self.assertEqual(len(mail.outbox), 0)

    send_campaign(email_list=users, threaded=False)

    self.assertEqual(len(mail.outbox), 1)

  def test_digest_log(self):
    pass
