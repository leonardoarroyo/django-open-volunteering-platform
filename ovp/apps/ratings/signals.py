import datetime
import base64
import json
from django.utils import timezone
from ovp.apps.channels.cache import get_channel_setting
from ovp.apps.core.notifybox import notification_manager

from ovp.apps.projects.models import Project
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from ovp.apps.ratings.models import Rating
from ovp.apps.ratings.models import RatingRequest
from ovp.apps.ratings.models import RatingParameter
from ovp.apps.ratings.models import RatingAnswer
from ovp.apps.projects.models import Job

def get_or_create_parameter(slug, type, channel):
    try:
        return RatingParameter.objects.get(slug=slug, channel__slug=channel)
    except RatingParameter.DoesNotExist:
        return RatingParameter.objects.create(slug=slug, type=type, object_channel=channel)

def create_rating_request(sender, *args, **kwargs):
  """
  Create rating request when project is closed
  """
  instance = kwargs["instance"]

  if not kwargs["raw"]:
      channel = instance.channel.slug
      enabled = get_channel_setting(channel, "ENABLE_USER_PRESENCE_RATING_REQUEST")[0] == "1"
      if (instance.closed == True and
           instance.pk and
           Project.objects.get(pk=instance.pk).closed == False and
           enabled):
          notifybox_client = notification_manager.get_client(channel)
          for apply in instance.apply_set.all():
              req = RatingRequest.objects.create(requested_user=apply.user, rated_object=instance, initiator_object=instance, object_channel=instance.channel.slug)
              req.rating_parameters.add(get_or_create_parameter("user-participated", 3, channel))
              req.rating_parameters.add(get_or_create_parameter("user-opinion", 1, channel))
              req.rating_parameters.add(get_or_create_parameter("user-project-rating", 2, channel))
              if apply.user:
                  diff = timezone.now() - apply.date
                  notification_manager.trigger(
                      channel,
                      "ratingRequested",
                      {
                          "project_title": apply.project.name,
                          "project_image": apply.project.image.image_small if (apply.project.image
                                                and apply.project.image.image_small) else "",
                          "days_diff": diff.days,
                          "days_diff_is_one": diff.days == 1,
                          "token": str(req.permission_token),
                          "request_uuid": str(req.uuid),
                          "pixel": str(
                              base64.b64encode(
                                  json.dumps({
                                      "source": "rating-request",
                                      "meta": json.dumps({
                                          "channel": channel,
                                          "project": apply.project.slug
                                      })
                                  }).encode("utf-8")
                              ),
                              "utf-8"
                          )
                      },
                      {},
                      [{
                          "recipient": f"user#{apply.user.uuid}",
                          "via": "app",
                          "type": "default"
                      },
                      {
                          "recipient": apply.user.email,
                          "via": "email",
                          "type": "default"
                      }]
                  )

pre_save.connect(create_rating_request, sender=Project)
