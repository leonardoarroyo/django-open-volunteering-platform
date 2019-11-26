from django.db.models import Q
from rest_framework import permissions

from ovp.apps.organizations.models import Organization

from ovp.apps.projects.models import Project

from django.shortcuts import get_object_or_404


##############################
# Project Resource permissions
##############################

class ProjectCreateOwnsOrIsOrganizationMember(permissions.BasePermission):
    """
    Permission that only allows an organization owner or member to create
    a project for the given organization.
    """

    def has_permission(self, request, view):
        organization_pk = request.data.get('organization_id', None)

        if not organization_pk:
            return True

        if not isinstance(organization_pk, int):
            return True  # Should fail on validator

        try:
            organization = Organization.objects.get(pk=organization_pk)
            if (organization.owner
                    == request.user
                    or request.user
                    in organization.members.all()):
                return True
        except Organization.DoesNotExist:  # pragma: no cover
            pass
        return False


class ProjectRetrieveOwnsOrIsOrganizationMember(permissions.BasePermission):
    """
    Permission that only allows the project owner, organization owner
    or organization member to retrieve/modify a existing project.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.owner == request.user:
                return True
            if obj.organization:
                if (request.user
                        in obj.organization.members.all()
                        or request.user == obj.organization.owner):
                    return True
        return False


##############################
# Apply Resource permissions
##############################

class ProjectApplyPermission(permissions.BasePermission):
    """
    Permission that only allows the project owner, organization owner
    or organization member to retrieve a full list of applies for a project.
    """

    def has_permission(self, request, view):
        project = get_object_or_404(
            Project,
            slug=view.kwargs.get("project_slug")
        )

        if request.user.is_authenticated:
            if request.user == project.owner:
                return True
            if project.organization:
                if (request.user
                        in project.organization.members.all()
                        or request.user == project.organization.owner):
                    return True
        return False

class ReapplyPermission(permissions.BasePermission):
    """
    Permission that only allows a user to apply/reapply if the user was
    not removed from project by organization.
    """

    def has_permission(self, request, view):
        project = get_object_or_404(
            Project,
            slug=view.kwargs.get("project_slug")
        )
        email = request.data.get("email", None)
        user = request.user if request.user.is_authenticated else None

        q_obj = Q()
        if email:
          q_obj.add(Q(email=email), Q.OR)
        if user:
          q_obj.add(Q(user=user), Q.OR)


        return not bool(
            project.apply_set.filter(
              q_obj,
              status__in=["confirmed-volunteer", "unapplied-by-organization"]
            ).count()
        )
