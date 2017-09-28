from django.test import TestCase

from django.core.cache import cache

from ovp.apps.projects.models import Category

from ovp.apps.catalogue.cache import get_catalogue
from ovp.apps.catalogue.models import Catalogue
from ovp.apps.catalogue.models import Section
from ovp.apps.catalogue.models import SectionFilter

def setUp():
  category1 = Category.objects.create(name="Hot", object_channel="default")

  catalogue = Catalogue.objects.create(name="Home", slug="home", object_channel="default")
  section1 = Section.objects.create(name="Hot", slug="hot", catalogue=catalogue, object_channel="default")
  section1_filter = SectionFilter.objects.create(section=section1, type="CATEGORY", object_channel="default")
  section1_filter.filter.categories.add(category1)

  section2 = Section.objects.create(name="Get your hands dirty", slug="get-your-hands-dirty", catalogue=catalogue, object_channel="default")
  section3 = Section.objects.create(name="This week", slug="this-week", catalogue=catalogue, object_channel="default")

  cache.clear()

class CatalogueTestCase(TestCase):
  def setUp(self):
    setUp()

  def test_catalogue_caching(self):
    with self.assertNumQueries(5):
      # 4 from catalogue, section and section filters models
      # 1 from applied filters
      catalogue = get_catalogue("default", "home")
    self.assertEqual(len(catalogue["sections"]), 3)

    with self.assertNumQueries(0):
      catalogue2 = get_catalogue("default", "home")
    self.assertEqual(catalogue, catalogue2)

class CategoryFilterTestCase(TestCase):
  def setUp(self):
    setUp()

  def test_category_filter(self):
    pass
