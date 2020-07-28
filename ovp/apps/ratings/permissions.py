from rest_framework import permissions


class IsAuthenticatedOrHasPermissionToken(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        permission_token = request.headers.get('x-ovp-permission-token', None)
        return bool(request.user and request.user.is_authenticated) or bool(permission_token)

class UserCanRateRequest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permission_token = request.headers.get('x-ovp-permission-token', None)
        if request.user == obj.requested_user or\
           (permission_token and str(obj.permission_token) == permission_token):
            return True
        return False
