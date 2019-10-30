from multiprocessing.dummy import Pool as ThreadPool
from ovp.apps.digest.emails import DigestEmail
from ovp.apps.digest.models import PROJECT
from ovp.apps.digest.backends.base import BaseBackend

class SMTPBackend(BaseBackend):
  def send_email(self, v):
    recipient = v["email"]
    channel = v["channel"]

    v["uuid"] = self.create_digest_log(v)
    DigestEmail(recipient, channel, async_mail=False).sendDigest(v)

    print(".", end="", flush=True)

  def send_chunk(self, content):
    pool = ThreadPool(8)
    result = pool.map(self.send_email, content)
    print("")
