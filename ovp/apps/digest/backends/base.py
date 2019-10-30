from ovp.apps.digest.models import DigestLog
from ovp.apps.digest.models import DigestLogContent
from ovp.apps.digest.models import PROJECT

class BaseBackend():
  def __init__(self, channel):
    self.channel = channel

  def create_digest_log(self, data):
    recipient = data["email"]
    channel = data["channel"]
    campaign = data["campaign"]

    dlog = DigestLog.objects.create(recipient=recipient, campaign=campaign, object_channel=channel)
    for project in data["projects"]:
      DigestLogContent.objects.create(object_channel=channel, content_type=PROJECT, content_id=project["pk"], digest_log=dlog)

    return str(dlog.uuid)

  def send_chunk(self, content_map):
    raise NotImplementedError

  def send_email(self, data):
    raise NotImplementedError
