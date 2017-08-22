from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

def get_user_jwt(request):
  user = get_user(request)
  if user.is_authenticated():
    return user
  try:
    user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
    if user_jwt is not None:
      return user_jwt[0]
  except:
    pass
  return user


class ChannelMiddleware():
  """
  This middleware is responsible for two things:

  - Adding the channel slug to request object
  - If the user is authenticated, only allow requests to resources from the same channel

  """
  def __init__(self, get_response):
    self.get_response = get_response

  def _check_permissions(self, request):
    # https://github.com/GetBlimp/django-rest-framework-jwt/issues/45
    user = get_user_jwt(request)

    if user.is_authenticated():
      user_channel = user.channel.slug
      if request.channel != user_channel:
        return False

    return True

  def _add_channel(self, request):
    request.channel = request.META.get("HTTP_X_OVP_CHANNEL", "default").strip()
    return request

  def __call__(self, request):
    # Parse and add channel
    request = self._add_channel(request)

    # Check user
    if not self._check_permissions(request):
      response = JsonResponse({"detail": "Invalid channel for user token."}, status=400)
    else:
      # Process request
      response = self.get_response(request)

    # Add channel header to response
    response["X-OVP-Channel"] = request.channel
    return response
