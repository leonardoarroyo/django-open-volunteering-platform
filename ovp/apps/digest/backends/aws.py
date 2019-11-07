import boto3
import json
from uuid import uuid4
from ovp.apps.projects.models import Work, Job
from ovp.apps.core.emails import BaseMail
from ovp.apps.digest.models import DigestLog
from ovp.apps.digest.models import DigestLogContent
from ovp.apps.digest.emails import DigestEmail
from ovp.apps.digest.models import PROJECT
from ovp.apps.digest.backends.base import BaseBackend
from ovp.apps.core.helpers import get_email_subject


class AWSBackend(BaseBackend):
  def __init__(self, channel):
    self.channel = channel
    self.client = boto3.client('ses')

  def send_chunk(self, content, template_context):
    template_uuid = self._create_template(template_context)
    content = list(content)

    response=self.client.send_bulk_templated_email(
        Source='Atados <noreply@atados.email>',
        ReplyToAddresses=['noreply@atados.email'],
        ReturnPath='noreply@atados.email',
        Template=template_uuid,
        DefaultTemplateData=json.dumps({}),
        Destinations=self._generate_aws_destinations(content)
    )
    self._write_log(response, content)
    self._delete_template(template_uuid)
    return self._get_count(response)

  def _get_count(self, response):
    statuses=response['Status']
    count = {}

    for item in statuses:
      status = item['Status']
      if not count.get(status, None):
        count[status] = 1
      else:
        count[status] += 1

    return count

  def _write_log(self, response, content):
    statuses=response['Status']
    assert len(statuses) == len(list(content))

    content_status=zip(statuses, content)
    for item in content_status:
      status = item[0]['Status']
      if status == 'Success':
        self.create_digest_log(item[1])
      else:
        pass # TODO: Log?

  def _generate_aws_destinations(self, content):
    aws_destinations = []
    for message in content:
      recipient = message['email']

      # Fix instance to str
      for i, project in enumerate(message["projects"]):
        message["projects"][i]["disponibility"] = project["disponibility"].start_date.strftime('%d/%m/%y às %H:%M') if isinstance(project["disponibility"], Job) and project["disponibility"].start_date is not None else ('Recorrente' if isinstance(project["disponibility"], Work) else "")
        message["projects"][i]["image"] = project["image"] if project["image_absolute"] else "https://atados-v3.storage.googleapis.com/{}".format(project["image"])

      aws_destinations.append({
        'Destination': {
            'ToAddresses': [recipient],
        },
        'ReplacementTemplateData': json.dumps(message)
      })
    return aws_destinations

  def _create_template(self, template_context):
    m = BaseMail('', channel=self.channel)
    uuid = str(uuid4())
    self.client.create_template(
        Template={
          'TemplateName': uuid,
          'SubjectPart': get_email_subject(self.channel, 'userDigest-aws', 'New digest'),
          'TextPart': '',
          'HtmlPart': m._render('userDigest-aws', template_context)[1]
          }
        )
    return uuid

  def _delete_template(self, uuid):
    self.client.delete_template(TemplateName=uuid)
