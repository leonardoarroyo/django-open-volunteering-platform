from ovp_testimonials import models
from ovp_users.serializers import ShortUserPublicRetrieveSerializer, UserProjectRetrieveSerializer
from rest_framework import serializers
from ovp_uploads.serializers import UploadedImageSerializer

class TestimonialCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Testimonial
    fields = ["content", "rating", "user", "created_date", "image", "video"]
    read_only_fields = ["created_date"]

class TestimonialRetrieveSerializer(serializers.ModelSerializer):
  user = ShortUserPublicRetrieveSerializer
  image = UploadedImageSerializer()
  user = UserProjectRetrieveSerializer()

  class Meta:
    model = models.Testimonial
    fields = ["content", "rating", "user", "created_date", "image", "video"]
