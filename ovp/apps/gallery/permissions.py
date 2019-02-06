from rest_framework import permissions
from rest_framework import exceptions

from ovp.apps.gallery.models import Gallery

from django.shortcuts import get_object_or_404


##############################
# Project Resource permissions
##############################

class GalleryEditAllowed(permissions.BasePermission):
  """ Permission that only allows an gallery owner to edit the gallery. """

  def has_object_permission(self, request, view, obj):
    if request.user.is_authenticated:
      if obj.owner == request.user:
        return True
      raise exceptions.PermissionDenied() #403
    return False #401 #pragma: no cover

