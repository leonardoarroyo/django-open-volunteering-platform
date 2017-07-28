from ovp.apps.channels.models import Channel

class ChannelTestCase():
  def test_migrations_create_default_channel(self):
    self.assertTrue(Channel.objects.count() == 1)
    self.assertTrue(Channel.objects.first().name == "default")
