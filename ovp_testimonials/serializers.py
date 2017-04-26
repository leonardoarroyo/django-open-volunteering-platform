from ovp_testimonials import models
from rest_framework import serializers

class TestimonialCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Testimonial
    fields = ["content", "rating", "user", "created_date"]
    read_only_fields = ["created_date"]
