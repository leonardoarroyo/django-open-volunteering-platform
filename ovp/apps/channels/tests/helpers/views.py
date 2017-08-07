# Helper user view to test decorator restricts queryset
from rest_framework import mixins
from rest_framework import viewsets

from ovp.apps.channels.decorators import ChannelViewSet
from ovp.apps.channels.mixins import CreateModelWithChannelMixin

from ovp.apps.users.models import User
from ovp.apps.users.serializers import UserCreateSerializer

@ChannelViewSet
class ChannelDecoratorUserTestViewSet(CreateModelWithChannelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = User.objects.all().order_by("pk")
  serializer_class = UserCreateSerializer
