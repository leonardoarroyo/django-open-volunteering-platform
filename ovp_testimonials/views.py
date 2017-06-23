import os

from collections import namedtuple

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from ovp_testimonials import models
from ovp_testimonials import helpers
from ovp_testimonials import serializers

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

class TestimonialResource(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  TestimonialResource endpoint
  """
  queryset = models.Testimonial.objects.filter(published=True)

  def create(self, request, *args, **kwargs):
    s = helpers.get_settings('OVP_TESTIMONIALS')

    if s.get("YOUTUBE_API_INTEGRATION", None):
      title = s.get("YOUTUBE_TITLE", "Depoimento")
      description = s.get("YOUTUBE_DESCRIPTION", "Depoimento")
      category = s.get("YOUTUBE_CATEGORY", 1)
      keywords = s.get("YOUTUBE_KEYWORDS", "depoimentos")

      data = request.FILES.get('video', None)
      if data:
        path = default_storage.save('tmp_video', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        
        options = namedtuple('options',
          ('file', 'keywords', 'title', 'description', 'privacyStatus', 'logging_level', 'noauth_local_webserver', 'approval_prompt', 'category')
        )(tmp_file, keywords, title, description, 'unlisted', 'DEBUG', True, 'force', category) 

        youtube = helpers.get_authenticated_service(options)
        upload = helpers.initialize_upload(youtube, options)

        default_storage.delete(tmp_file)
        
        if "id" in upload:
          request.data["video"] = upload["id"]
        else:
          return Response({"error": True, "detail": "upload_video_failed", "message": "Upload Video Failed"}, status=400)
    
    if not helpers.get_settings().get("CAN_CREATE_TESTIMONIAL_UNAUTHENTICATED", False):
      request.data["user"] = request.user.pk

    return super(TestimonialResource, self).create(request, *args, **kwargs)

  def get_permissions(self):
    request = self.get_serializer_context()["request"]
    if self.action == "create":
      if helpers.get_settings().get("CAN_CREATE_TESTIMONIAL_UNAUTHENTICATED", False):
        self.permission_classes = ()
      else:
        self.permission_classes = (permissions.IsAuthenticated, )

    return super(TestimonialResource, self).get_permissions()

  def get_serializer_class(self):
    if self.action == "create":
      return serializers.TestimonialCreateSerializer
    return serializers.TestimonialRetrieveSerializer
