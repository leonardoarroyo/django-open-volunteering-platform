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

  - Adding the channels slug to request object
  - If the user is authenticated, only allow requests to resources from the same channel

  """
  def __init__(self, get_response):
    self.get_response = get_response

  def _check_permissions(self, request):
    if request.user.is_authenticated():
      user_channel = request.user.channel.slug
      for slug in request.channels:
        # TODO: Parent channel implementation
        if slug != user_channel:
          return False

    return True

  def _add_channels(self, request):
    self.channels = [x.strip() for x in request.META.get("HTTP_X_OVP_CHANNELS", "default").split(";")]
    request.channels = self.channels
    return request

  def __call__(self, request):
    # Parse and add channels
    request = self._add_channels(request)

    # Check user
    if not self._check_permissions(request):
      return JsonResponse({"detail": "Invalid channel for user token."}, status=400)

    # Process request
    response = self.get_response(request)

    # Add channels header to response
    response["X-OVP-Channels"] = ";".join(self.channels)
    return response
