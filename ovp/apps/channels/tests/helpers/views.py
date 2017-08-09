# Helper user view to test decorator restricts queryset
from rest_framework import mixins
from rest_framework import viewsets

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.channels.viewsets.mixins import CreateModelWithChannelMixin

from ovp.apps.users.models import User
from ovp.apps.users.serializers import UserCreateSerializer

from ovp.apps.projects.models.project import Project
from ovp.apps.projects.serializers.project import ProjectCreateUpdateSerializer

@ChannelViewSet
class ChannelUserTestViewSet(CreateModelWithChannelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = User.objects.all().order_by("pk")
  serializer_class = UserCreateSerializer

@ChannelViewSet
class ChannelProjectTestViewSet(CreateModelWithChannelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = Project.objects.all().order_by("pk")
  serializer_class = ProjectCreateUpdateSerializer