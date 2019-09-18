# test filter sent recently
# test filter no content
from django.test import TestCase
from ovp.apps.channels.models import Channel
from ovp.apps.digest.digest import get_filtered_list
from ovp.apps.digest.digest import generate_content
from ovp.apps.search.tests.test_views import create_sample_projects
from ovp.apps.search.tests.test_views import create_sample_users

class DigestTestCase(TestCase):
  def setUp(self):
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_projects()
    create_sample_users()

  def test_filter_sent_recently(self):
    pass

  def test_filter_no_new_content(self):
    pass

  def test_num_queries_generate_content(self):
    email_list = ["testmail1@test.com"]
    with self.assertNumQueries(5):
      content = generate_content(email_list, channel="default")

    # Only one query per user
    email_list = ["testmail1@test.com", "testmail2@test.com"]
    with self.assertNumQueries(6):
      content = generate_content(email_list, channel="default")
