from django.test import TestCase
from django.core.cache import cache
from ovp.apps.channels.models.channel_setting import ChannelSetting
from ovp.apps.channels.cache import get_channel

class ChannelCacheTestCase(TestCase):
  def setUp(self):
    cache.clear()

  def test_channel_cache(self):
    with self.assertNumQueries(2):
      channel = get_channel("default")
    with self.assertNumQueries(0):
      channel = get_channel("default")

  def test_channel_cache_settings(self):
    ChannelSetting.objects.create(key="test-setting", value="test-val", object_channel="default")
    ChannelSetting.objects.create(key="test-setting2", value="test-val", object_channel="default")

    with self.assertNumQueries(2):
      channel = get_channel("default")
    with self.assertNumQueries(0):
      channel = get_channel("default")

    self.assertTrue(len(channel["settings"]) == 2)
