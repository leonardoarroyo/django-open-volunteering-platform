from ovp.apps.users.models import User

from ovp.apps.core.serializers import EmptySerializer
from ovp.apps.core.mixins import BookmarkMixin

from django.core.exceptions import ValidationError
from ovp.apps.organizations import serializers
from ovp.apps.organizations import models
from ovp.apps.organizations import permissions as organization_permissions
from ovp.apps.organizations.validators import format_CNPJ, validate_CNPJ

from ovp.apps.projects.serializers.project import ProjectOnOrganizationRetrieveSerializer
from ovp.apps.projects.models import Project

from ovp.apps.uploads import models as upload_models

from ovp.apps.channels.viewsets.decorators import ChannelViewSet


from rest_framework import decorators
from rest_framework import viewsets
from rest_framework import response
from rest_framework import mixins
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404


import json

@ChannelViewSet
class OrganizationResourceViewSet(BookmarkMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  OrganizationResourceViewSet resource endpoint
  """
  queryset = models.Organization.objects.all()
  model = models.Organization
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  def partial_update(self, request, *args, **kwargs):
    """ We do not include the mixin as we want only PATCH and no PUT """
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if getattr(instance, '_prefetched_objects_cache', None): #pragma: no cover
      instance = self.get_object()
      serializer = self.get_serializer(instance)

    return response.Response(serializer.data)

  @decorators.list_route(methods=["GET"], url_path='check-doc/(?P<doc>[0-9]+)')
  def check_doc(self, request, doc):
    formatted_doc = format_CNPJ(doc)
    try:
      validate_CNPJ(formatted_doc)
    except ValidationError as validation_error:
      return response.Response({ "invalid": True, "message": validation_error.message }, status=400)
    except:
      return response.Response({ "invalid": True }, status=400)

    taken = models.Organization.objects.filter(document=formatted_doc, channel__slug=request.channel).count() > 0
    return response.Response({ "taken": taken })

  @decorators.detail_route(methods=["GET"])
  def pending_invites(self, request, *args, **kwargs):
    organization = self.get_object()
    invites = organization.organizationinvite_set.all()
    serializer = self.get_serializer(invites, many=True)

    return response.Response(serializer.data)

  @decorators.detail_route(methods=["POST"])
  def invite_user(self, request, *args, **kwargs):
    organization = self.get_object()

    serializer = self.get_serializer_class()(data=request.data)
    serializer.is_valid(raise_exception=True)

    invited = User.objects.get(email=request.data["email"], channel__slug=request.channel)

    try:
      models.OrganizationInvite.objects.get(organization=organization, invited=invited, channel__slug=request.channel)
      return response.Response({"email": ["This user is already invited to this organization."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      pass

    invite = models.OrganizationInvite(invitator=request.user, invited=invited, organization=organization)
    invite.save(object_channel=request.channel)

    organization.mailing().sendUserInvited(context={"invite": invite})

    return response.Response({"detail": "User invited."})

  @decorators.detail_route(methods=["POST"])
  def join(self, request, *args, **kwargs):
    organization = self.get_object()
    organization.members.add(request.user)

    organization.mailing().sendUserJoined(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "Joined organization."})

  @decorators.detail_route(methods=["POST"])
  def revoke_invite(self, request, *args, **kwargs):
    organization = self.get_object()

    try:
      try:
        user = User.objects.get(email=request.data.get("email", ""), channel__slug=request.channel)
        invite = models.OrganizationInvite.objects.get(invited=user, organization=organization, channel__slug=request.channel)
      except User.DoesNotExist:
        return response.Response({"email": ["This user is not valid."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      return response.Response({"detail": "This user is not invited to this organization."}, status=400)

    organization.mailing().sendUserInvitationRevoked(context={"invite": invite})
    invite.delete()

    return response.Response({"detail": "Invite has been revoked."})

  @decorators.detail_route(methods=["POST"])
  def leave(self, request, *args, **kwargs):
    organization = self.get_object()
    organization.members.remove(request.user)

    organization.mailing().sendUserLeft(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "You've left the organization."})

  @decorators.detail_route(methods=["POST"])
  def remove_member(self, request, *args, **kwargs):
    organization = self.get_object()
    serializer = self.get_serializer_class()

    try:
      user = organization.members.get(email=request.data.get("email", ""))
    except User.DoesNotExist:
      return response.Response({"email": ["This user is not valid."]}, status=400)

    organization.members.remove(user)

    organization.mailing().sendUserRemoved(context={"user": user, "organization": organization})

    return response.Response({"detail": "Member was removed."})

  @decorators.detail_route(methods=["GET"])
  def members(self, request, *args, **kwargs):
    organization = self.get_object()
    members = User.objects.filter(pk=organization.owner.pk) | organization.members.all()
    serializer = self.get_serializer(members, many=True)
    return response.Response(serializer.data)

  @decorators.detail_route(methods=['GET'])
  def projects(self, request, slug, pk=None):
    organization = self.get_object()
    projects = Project.objects.filter(organization=organization, published=True)
    page = self.paginate_queryset(projects)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer(projects, many=True)

    return response.Response(serializer.data)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.deleted:
      content = {'detail': 'This project was deleted'}
      return response.Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
      serializer = self.get_serializer(instance)
      return response.Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def create(self, request, *args, **kwargs):
    request.data['owner'] = request.user.id

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    organization = serializer.save()
    organization.members.add(request.user)

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  ###################
  # ViewSet methods #
  ###################
  def get_bookmark_model(self):
    return models.OrganizationBookmark

  def get_bookmark_kwargs(self):
    return {"organization": self.get_object()}

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']
    if self.action in ['create', 'partial_update']:
      return serializers.OrganizationCreateSerializer
    if self.action == 'retrieve':
      return serializers.OrganizationRetrieveSerializer
    if self.action == 'pending_invites':
      return serializers.OrganizationInviteRetrieveSerializer
    if self.action in ['invite_user', 'revoke_invite']:
      return serializers.OrganizationInviteSerializer
    if self.action == 'remove_member':
      return serializers.MemberRemoveSerializer
    if self.action == 'projects':
      return ProjectOnOrganizationRetrieveSerializer
    if self.action in ['bookmarked']:
      return serializers.OrganizationRetrieveSerializer
    if self.action == 'members':
      return serializers.MemberListRetrieveSerializer
    if self.action in ['leave', 'join']: # pragma: no cover
      return EmptySerializer

  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == 'partial_update':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action == 'retrieve':
      self.permission_classes = ()
    if self.action in ['pending_invites', 'invite_user', 'revoke_invite']:
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action == 'join':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.IsInvitedToOrganization)
    if self.action == 'leave':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.IsOrganizationMember)
    if self.action == 'remove_member':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrganization)
    if self.action == 'members':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action in ['bookmark', 'unbookmark', 'bookmarked']:
      self.permission_classes = self.get_bookmark_permissions()

    return super(OrganizationResourceViewSet, self).get_permissions()
