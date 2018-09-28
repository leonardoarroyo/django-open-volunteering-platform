from rest_framework import serializers

class TokenViewSerializer(serializers.Serializer):
  token = serializers.CharField()

  class Meta:
    fields = ["token"]