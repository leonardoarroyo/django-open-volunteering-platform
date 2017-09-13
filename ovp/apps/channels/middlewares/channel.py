from ovp.apps.channels.cache import get_channel

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.http import JsonResponse
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

import urllib.parse as parse

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
  This middleware is responsible for three things:

  - Adding the channel slug to request object
  - If the user is authenticated, only allow requests to resources from the same channel
  - Check if the requested channel is valid
  - Redirects to / if the path starts with /admin/ or /jet/

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

  def _404(self, request):
    path = request.get_full_path()
    if path.startswith("/admin") or path.startswith("/jet"):
      raise Http404
    return False

  def __call__(self, request):
    if request.is_admin_page:
      # The request has been treated by the ChannelAdminMiddleware
      return self.get_response(request)

    # Parse and add channel
    request = self._add_channel(request)

    # Redirect 404 if trying to access admin without going through a channel subdomain
    self._404(request)

    # Check channel is valid
    if get_channel(request.channel) is None:
      return JsonResponse({"detail": "Invalid channel."}, status=400)

    # Check user
    if not self._check_permissions(request):
      response = JsonResponse({"detail": "Invalid channel for user token."}, status=400)
    else:
      # Process request
      response = self.get_response(request)

    # Add channel header to response
    response["X-OVP-Channel"] = request.channel
    return response


class ChannelAdminMiddleware():
  """
  This middleware is responsible for three things:

  - Adding the channel slug to request object if it's a request to admin
  - Blocking requests to admin that does not include channel
  - Redirects to /admin/ if the path does not start with /admin/ or /jet/

  """
  def __init__(self, get_response):
    self.get_response = get_response

  def _is_admin_request(self, request):
    absolute_url = request.build_absolute_uri(request.get_full_path())
    parsed_url = parse.urlparse(absolute_url)
    domains = parsed_url.netloc.split(".")

    if len(domains) >= 3 and "admin" == domains[1]:
      return True, domains[0]

    return False, None

  def _add_channel(self, request):
    is_admin, channel = self._is_admin_request(request)

    request.is_admin_page = False
    if is_admin:
      request.is_admin_page = True
      request.channel = channel

    return request

  def _redirect(self, request):
    path = request.get_full_path()
    if not path.startswith("/admin") and not path.startswith("/jet") and not path.startswith("/static"):
      return True

    return False

  def __call__(self, request):
    # Parse and add channel
    request = self._add_channel(request)

    if request.is_admin_page:
      # Check channel is valid
      if get_channel(request.channel) is None:
        return HttpResponse("Invalid channel.", status=400)

      # Redirect if not on admin page
      if self._redirect(request):
        return redirect("/admin")

      response = self.get_response(request)

      # Add channel header to response
      response["X-OVP-Channel"] = request.channel
      return response

    return self.get_response(request)
