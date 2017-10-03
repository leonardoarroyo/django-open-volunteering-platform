from django.test import TestCase
from django.core.cache import cache
from django.db.models.query import QuerySet

from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnList

from ovp.apps.users.models import User

from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Category
from ovp.apps.projects.serializers.project import ProjectSearchSerializer

from ovp.apps.catalogue.cache import get_catalogue
from ovp.apps.catalogue.cache import fetch_catalogue
from ovp.apps.catalogue.models import Catalogue
from ovp.apps.catalogue.models import Section
from ovp.apps.catalogue.models import SectionFilter

def setUp():
  # Categories
  category1 = Category.objects.create(name="Hot", object_channel="default")
  category2 = Category.objects.create(name="Get your hands dirty", object_channel="default")

  # Catalogue
  catalogue = Catalogue.objects.create(name="Home", slug="home", object_channel="default")

  # Sections
  section1 = Section.objects.create(name="Hot", slug="hot", catalogue=catalogue, object_channel="default")
  section1_filter = SectionFilter.objects.create(section=section1, type="CATEGORY", object_channel="default")
  section1_filter.filter.categories.add(category1)

  section2 = Section.objects.create(name="Get your hands dirty", slug="get-your-hands-dirty", catalogue=catalogue, object_channel="default")
  section2_filter = SectionFilter.objects.create(section=section2, type="CATEGORY", object_channel="default")
  section2_filter.filter.categories.add(category2)

  section3 = Section.objects.create(name="This week", slug="this-week", catalogue=catalogue, object_channel="default")

  # Projects
  user = User.objects.create(email="sample@user.com", password="sample-user", object_channel="default")
  project1 = Project.objects.create(name="sample 1", owner=user, description="description", details="detail", object_channel="default", published=True)
  project1.categories.add(category1)

  project2 = Project.objects.create(name="sample 2", owner=user, description="description", details="detail", object_channel="default", published=True)
  project2.categories.add(category2)

  cache.clear()

class CatalogueCacheTestCase(TestCase):
  def setUp(self):
    setUp()

  def test_get_catalogue_caching(self):
    with self.assertNumQueries(7):
      # 4 from catalogue, section and section filters models
      # 2 from applied filters(category 1)
      # 2 from applied filters(category 2)
      # 0 from applied filters(category 3)
      catalogue = get_catalogue("default", "home")
    self.assertEqual(len(catalogue["sections"]), 3)

    with self.assertNumQueries(0):
      catalogue2 = get_catalogue("default", "home")
    self.assertEqual(catalogue, catalogue2)

  def test_fetch_catalogue_num_queries(self):
    catalogue = get_catalogue("default", "home")

    with self.assertNumQueries(12):
      # 4 queries for each section(projects + skills + causes + categories)
      # We have 3 sections on the test case, so there are 12 queries
      fetched = fetch_catalogue(catalogue, serializer=ProjectSearchSerializer)

  def test_fetch_queryset_without_serializer(self):
    catalogue = get_catalogue("default", "home")
    fetched = fetch_catalogue(catalogue)

    self.assertEqual(fetched["sections"][0]["projects"].__class__, QuerySet)

  def test_fetch_queryset_with_serializer(self):
    catalogue = get_catalogue("default", "home")
    fetched = fetch_catalogue(catalogue, serializer=ProjectSearchSerializer)

    self.assertEqual(fetched["sections"][0]["projects"].__class__, ReturnList)

class CatalogueViewTestCase(TestCase):
  def setUp(self):
    setUp()
    self.client = APIClient()

  def test_view_404(self):
    response = self.client.get(reverse("catalogue", ["invalid"]), format="json")
    self.assertEqual(response.status_code, 404)

  def test_view_200(self):
    response = self.client.get(reverse("catalogue", ["home"]), format="json")
    self.assertEqual(response.status_code, 200)

  def test_is_bookmarked(self):
    response = self.client.get(reverse("catalogue", ["home"]), format="json")
    self.assertTrue("is_bookmarked" in response.data["sections"][0]["projects"][0])

class CategoryFilterTestCase(TestCase):
  def setUp(self):
    setUp()
    self.client = APIClient()

  def test_category_filter(self):
    response = self.client.get(reverse("catalogue", ["home"]), format="json")
    self.assertEqual(len(response.data["sections"][0]["projects"]), 1)
    self.assertEqual(response.data["sections"][0]["projects"][0]["name"], "sample 1")

    self.assertEqual(len(response.data["sections"][1]["projects"]), 1)
    self.assertEqual(response.data["sections"][1]["projects"][0]["name"], "sample 2")

# TODO: Date filter
