from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from dateutil.relativedelta import relativedelta

from ovp.apps.users import serializers
from ovp.apps.users import models

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema

@ChannelViewSet
class RecoveryTokenViewSet(viewsets.GenericViewSet):
  """
  RecoveryToken resource endpoint
  """
  queryset = models.User.objects.all()
  serializer_class = serializers.RecoveryTokenSerializer

  @swagger_auto_schema(responses={200: 'OK', 429: 'Too many requests.'})
  def create(self, request, *args, **kwargs):
    """ Request a password recovery token. An email will be dispatched if the user is registered on the platform. """
    email = request.data.get('email', None)

    try:
      user = self.get_queryset().get(email__iexact=email)
    except:
      user = None

    if user:
      # Allow only 5 requests per hour
      limit = 5
      now = timezone.now()
      to_check = (now - relativedelta(hours=1)).replace(tzinfo=timezone.utc)
      tokens = models.PasswordRecoveryToken.objects.filter(user=user, created_date__gte=to_check, channel__slug=request.channel)

      if tokens.count() >= limit:
        will_release = tokens.order_by('-created_date')[limit-1].created_date + relativedelta(hours=1)
        seconds = abs((will_release - now).seconds)
        return response.Response({'success': False, 'message': 'Five tokens generated last hour.', 'try_again_in': seconds}, status=status.HTTP_429_TOO_MANY_REQUESTS)

      token = models.PasswordRecoveryToken.objects.create(user=user, object_channel=request.channel)

    return response.Response({'success': True, 'message': 'Token requested successfully(if user exists).'})


@ChannelViewSet
class RecoverPasswordViewSet(viewsets.GenericViewSet):
  """
  RecoverPassword resource endpoint
  """
  queryset = models.PasswordRecoveryToken.objects.all()
  serializer_class = serializers.RecoverPasswordSerializer

  @swagger_auto_schema(responses={200: 'OK', 400: 'Bad request', 401: 'Unauthorized'})
  def create(self, request, *args, **kwargs):
    """ Update user password using recovery token. """
    token = request.data.get('token', None)
    new_password = request.data.get('new_password', None)
    day_ago = (timezone.now() - relativedelta(hours=24)).replace(tzinfo=timezone.utc)

    try:
      rt = self.get_queryset().get(token=token)
    except:
      rt = None

    if (not rt) or rt.used_date or rt.created_date < day_ago:
      return response.Response({'message': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not new_password:
      return response.Response({'message': 'Empty password not allowed.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      validate_password(new_password, user=rt.user)
    except ValidationError as e:
      return response.Response({'message': 'Invalid password.', 'errors': e}, status=status.HTTP_400_BAD_REQUEST)

    serializers.RecoverPasswordSerializer(data=request.data, context=self.get_serializer_context()).is_valid(raise_exception=True)

    rt.used_date=timezone.now()
    rt.save()

    rt.user.password = new_password
    rt.user.save()

    return response.Response({'message': 'Password updated.'})
