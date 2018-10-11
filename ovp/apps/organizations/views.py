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
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.utils import timezone


import json

@ChannelViewSet
class OrganizationResourceViewSet(BookmarkMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  Create, modify, retrieve and manage organizations.
  """
  queryset = models.Organization.objects.filter(deleted=False)
  model = models.Organization
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  def retrieve(self, *args, **kwargs):
    """ Retrieve an organization. """
    return super(OrganizationResourceViewSet, self).retrieve(*args, **kwargs)

  def partial_update(self, request, *args, **kwargs):
    """ Partially update an organization object. """
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if getattr(instance, '_prefetched_objects_cache', None): #pragma: no cover
      instance = self.get_object()
      serializer = self.get_serializer(instance)

    return response.Response(serializer.data)

  @swagger_auto_schema(method="GET", responses={200: 'OK', 400: 'Invalid'})
  @decorators.list_route(methods=["GET"], url_path='check-doc/(?P<doc>[0-9]+)')
  def check_doc(self, request, doc):
    """ Check if there is an organization with a given document. """
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
    """ Retrieve list of pending invites for organization. """
    organization = self.get_object()
    invites = organization.organizationinvite_set.filter(joined_date=None, revoked_date=None)
    serializer = self.get_serializer(invites, many=True)

    return response.Response(serializer.data)

  @swagger_auto_schema(method="POST", responses={200: 'OK', 400: 'Invalid invite'})
  @decorators.detail_route(methods=["POST"])
  def invite_user(self, request, *args, **kwargs):
    """ Invite user to manage organization. The supplied email address must be registered. """
    organization = self.get_object()

    serializer = self.get_serializer_class()(data=request.data)
    serializer.is_valid(raise_exception=True)

    invited = User.objects.get(email=request.data["email"], channel__slug=request.channel)

    if organization.members.filter(pk=invited.pk).count():
      return response.Response({"email": ["This user is already part of this organization."]}, status=400)

    try:
      models.OrganizationInvite.objects.get(organization=organization, invited=invited, joined_date=None, revoked_date=None, channel__slug=request.channel)
      return response.Response({"email": ["This user is already invited to this organization."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      pass

    invite = models.OrganizationInvite(invitator=request.user, invited=invited, organization=organization)
    invite.save(object_channel=request.channel)

    organization.mailing().sendUserInvited(context={"invite": invite})

    return response.Response({"detail": "User invited."})

  @swagger_auto_schema(method="POST", responses={200: 'OK', 403: 'Forbidden'})
  @decorators.detail_route(methods=["POST"])
  def join(self, request, *args, **kwargs):
    """ Join an organization you have been invited to manage. """
    organization = self.get_object()
    organization.members.add(request.user)

    invite = models.OrganizationInvite.objects.get(organization=organization, invited=request.user, joined_date=None, revoked_date=None, channel__slug=request.channel)
    invite.joined_date = timezone.now()
    invite.save()

    organization.mailing().sendUserJoined(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "Joined organization."})

  @swagger_auto_schema(method="POST", responses={200: 'OK', 400: 'Invalid invite'})
  @decorators.detail_route(methods=["POST"])
  def revoke_invite(self, request, *args, **kwargs):
    """ Revoke an invite made to another user. """
    organization = self.get_object()

    try:
      try:
        user = User.objects.get(email=request.data.get("email", ""), channel__slug=request.channel)
        invite = models.OrganizationInvite.objects.get(invited=user, organization=organization, joined_date=None, revoked_date=None, channel__slug=request.channel)
      except User.DoesNotExist:
        return response.Response({"email": ["This user is not valid."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      return response.Response({"detail": "There is no pending invites for this user in this organization."}, status=400)

    invite.revoked_date = timezone.now()
    invite.save()
    organization.mailing().sendUserInvitationRevoked(context={"invite": invite})

    return response.Response({"detail": "Invite has been revoked."})

  @swagger_auto_schema(method="POST", responses={200: 'OK', 403: 'Forbidden'})
  @decorators.detail_route(methods=["POST"])
  def leave(self, request, *args, **kwargs):
    """ Leave an organization you are member of. """
    organization = self.get_object()
    organization.members.remove(request.user)

    organization.mailing().sendUserLeft(context={"user": request.user, "organization": organization})

    return response.Response({"detail": "You've left the organization."})

  @swagger_auto_schema(method="POST", responses={200: 'OK', 400: 'Invalid user', 403: 'Forbidden'})
  @decorators.detail_route(methods=["POST"])
  def remove_member(self, request, *args, **kwargs):
    """ Remove another user from organization. """
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
    """ Retrieve list of members in an organization. """
    organization = self.get_object()
    members = organization.members.all()
    serializer = self.get_serializer(members, many=True)
    return response.Response(serializer.data)

  @decorators.detail_route(methods=['GET'])
  def projects(self, request, slug, pk=None):
    """ Retrieve a list of projects an organization manages. """
    organization = self.get_object()
    projects = Project.objects.filter(organization=organization, published=True)
    page = self.paginate_queryset(projects)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer(projects, many=True)

    return response.Response(serializer.data)

  def create(self, request, *args, **kwargs):
    """ Create an organization. """
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
