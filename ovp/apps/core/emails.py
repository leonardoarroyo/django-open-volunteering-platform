import threading, sys
import boto3
from botocore.exceptions import ClientError

from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings
from django.utils import translation

from ovp.apps.core.helpers import is_email_enabled, get_email_subject
from ovp.apps.channels.cache import get_channel_setting

class BaseMail:
  """
  This class is responsible for firing emails
  """
  aws_access_key = getattr(settings, "AWS_ACCESS_KEY")
  aws_secret_key = getattr(settings, "AWS_SECRET_KEY")
  aws_region = getattr(settings, "AWS_REGION")
  from_email = getattr(settings, "SENDER")

  def __init__(self, email_address, channel=None, async_mail=None, locale=None):
    self.channel = channel
    self.email_address = email_address
    self.async_mail = async_mail

  def sendEmail(self, template_name, subject, context={}):
    if not is_email_enabled(self.channel, template_name):
      return False

    # Inject extra context
    ctx = inject_client_url(self.channel, context)
    ctx["extend"] = {
      "html": "{}/email/base-body.html".format(self.channel),
      "txt": "{}/email/base-body.txt".format(self.channel)
    }

    subject = get_email_subject(self.channel, template_name, subject)
    text_content, html_content = self.__render(template_name, ctx)
    charset = "UTF-8"

    message = {}
    message.setdefault('Body', {})
    message.setdefault('Subject', {})

    message['Body']['Html'] = {'Charset': charset, 'Data': html_content}
    message['Body']['Text'] = {'Charset': charset, 'Data': text_content}
    message['Subject'] = {'Charset': charset, 'Data': subject}

    client = boto3.client(
      'ses',
      aws_access_key_id=self.aws_access_key, 
      aws_secret_access_key=self.aws_secret_key, 
      region_name=self.aws_region
    )
     # Try to send the email.
    try:
      #Provide the contents of the email.
      response = client.send_email(
        Destination={'ToAddresses': [self.email_address]},
        Message=message,
        Source=self.from_email,
      )
    # Display an error if something goes wrong.	
    except ClientError as e:
      print(e.response['Error']['Message'])

  def __render(self, template_name, ctx):
    test_channels = getattr(settings, "TEST_CHANNELS", [])

    try:
      text_content = get_template('{}/email/{}-body.txt'.format(self.channel, template_name)).render(ctx)
      html_content = get_template('{}/email/{}-body.html'.format(self.channel, template_name)).render(ctx)
    except TemplateDoesNotExist as e:
      # This avoids template errors when testing with non-default channel
      if self.channel in test_channels:
        return ("", "")

      # Re-raise if not a test channel
      raise(e)

    return (text_content, html_content)

class ContactFormMail(BaseMail):
  """
  This class is reponsible for firing emails sent through the contact form
  """
  def __init__(self, recipients, channel=None, async_mail=None, locale=None):
    self.channel = channel
    self.recipients = recipients
    self.async = async_mail
    self.locale = locale

  def sendContact(self, context={}):
    """
    Send contact form message to single or multiple recipients
    """
    for recipient in self.recipients:
      super(ContactFormMail, self).__init__(recipient, channel=self.channel, async_mail=self.async, locale=self.locale)
      self.sendEmail('contactForm', 'New contact form message', context)


#
# Helpers
#

def inject_client_url(channel, ctx):
  ctx['CLIENT_URL'] = get_channel_setting(channel, "CLIENT_URL")[0]
  return ctx
