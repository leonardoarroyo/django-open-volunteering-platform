from django.conf import settings

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

def get_settings(string="OVP_TESTIMONIALS"):
  return getattr(settings, string, {})


httplib2.RETRIES = 1

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at: %s
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)),
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage(os.path.abspath(os.path.join(os.path.dirname(__file__), "youtube-oauth2.json")))
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category
    ),
    status=dict(
      privacyStatus=options.privacyStatus
    )
  )

  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
  )

  status, response = insert_request.next_chunk()
  return response