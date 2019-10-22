from multiprocessing.dummy import Pool as ThreadPool
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from ovp.apps.projects.models import Project
from ovp.apps.digest.emails import DigestEmail
from ovp.apps.digest.models import DigestLog
from ovp.apps.digest.models import DigestLogContent
from ovp.apps.digest.models import PROJECT
from ovp.apps.users.models import User
from ovp.apps.search.filters import UserSkillsCausesFilter
from ovp.apps.uploads import helpers
from django.db.models import Value, IntegerField

import time
import math

config = {
  'interval': {
    'minimum': 60 * 60 * 24 * 6,
    'maximum': 0
  },
  'projects': {
    'minimum': 1,
    'maximum': 6,
    'max_age': 60 * 60 * 24 * 7 * 4,
  }
}

def send_email(v):
  recipient = v["email"]
  channel = v["channel"]
  campaign = v["campaign"]

  dlog = DigestLog.objects.create(recipient=recipient, campaign=campaign, object_channel=channel)
  for project in v["projects"]:
    DigestLogContent.objects.create(object_channel=channel, content_type=PROJECT, content_id=project["pk"], digest_log=dlog)
  v["uuid"] = str(dlog.uuid)
  DigestEmail(recipient, channel, async_mail=False).sendDigest(v)
  print(".", end="", flush=True)

def send_campaign(chunk_size=0, channel="default", email_list=None):
  try:
    campaign = DigestLog.objects.order_by("-pk")[0].campaign + 1
  except:
    campaign = 1

  if not email_list:
    email_list = get_email_list(channel)

  user_list = list(pre_filter(email_list))

  if not len(user_list):
    print("0 users to send.")
    return

  try:
    chunks = math.ceil(len(user_list)/chunk_size)
  except ZeroDivisionError:
    chunks = 1
    chunk_size = len(user_list)

  if not len(user_list):
    return

  print("Sending campaign {}.\nChunk size: {}\nChunks: {}".format(campaign, chunk_size, chunks))

  for i in range(0, len(user_list), chunk_size):
      chunk_i = math.ceil(i/chunk_size) + 1

      print("Processing chunk {}/{}".format(chunk_i, chunks))
      chunk = user_list[i:i+chunk_size]
      content_map = generate_content(chunk, campaign)

      pool = ThreadPool(8)
      result = pool.map(send_email, content_map)
      print("")

def get_email_list(channel="default"):
  return set(
    User.objects
      .select_related('channel', 'users_userprofile_profile')
      .filter(channel__slug=channel, is_subscribed_to_newsletter=True)
      .values_list('email', flat=True)
  )

def pre_filter(email_list):
  sent_recently = set(
    DigestLog.objects
      .filter(trigger_date__gt=timezone.now() - relativedelta(seconds=config['interval']['minimum']))
      .values_list('recipient', flat=True)
  )
  return set(filter(lambda x: x not in sent_recently, email_list))


def generate_content(email_list, campaign, channel='default'):
  print("generating content")
  content_dict = {}

  print("fetching users")
  users = list(User.objects
    .prefetch_related('users_userprofile_profile__causes', 'users_userprofile_profile__skills')
    .select_related('channel')
    .filter(channel__slug=channel, email__in=email_list)
    .annotate(campaign=Value(campaign, IntegerField())))

  print("fetched users")

  pool = ThreadPool(8)
  result = pool.map_async(generate_content_for_user, users, chunksize=4)
  real_result = result.get()
  pool.close()
  pool.join()
  real_result = filter(lambda x: x != None, real_result)

  return real_result

def filter_by_address(qs, user):
  if not user.profile or not user.profile.address:
    return qs
  state = user.profile.address.address_components.filter(types__name="administrative_area_level_1").first()

  if not state:
    return qs
  state = state.short_name
  filtered_qs = qs.filter(address__address_components__short_name=state,
                   address__address_components__types__name="administrative_area_level_1")

  return filtered_qs if filtered_qs.count() > 0 else qs

def generate_content_for_user(user):
  not_projects = list(
    DigestLogContent.objects.filter(digest_log__recipient=user.email, content_type=PROJECT, channel=user.channel).values_list('content_id', flat=True)
  )
  projects = Project.objects \
    .filter(channel__slug=user.channel.slug, deleted=False, closed=False, published=True, published_date__gte=timezone.now() - relativedelta(seconds=config['projects']['max_age'])) \
    .exclude(pk__in=not_projects) \
    .select_related('image', 'job', 'work')
  projects = filter_by_address(projects, user)
  projects = UserSkillsCausesFilter() \
      .annotate_queryset(projects, user, no_check=True, append_assumed=True) \
      .order_by("-relevance")[:config["projects"]["maximum"]]

  if len(projects) < config["projects"]["minimum"]:
    return None

  return {
    "email": user.email,
    "channel": user.channel.slug,
    "campaign": user.campaign,
    "projects": [
      {
        "pk": p.pk,
        "name": p.name,
        "slug": p.slug,
        "description": p.description,
        "image": p.image.image_small if p.image and p.image.image_small else "",
        "image_absolute": p.image.absolute if p.image else False,
        "disponibility": p.job if hasattr(p, 'job') else (p.work if hasattr(p, 'work') else None),
        "disponibility_type": 'job' if hasattr(p, 'job') else ('work' if hasattr(p, 'work') else None)
      } for p in projects
    ]
  }
