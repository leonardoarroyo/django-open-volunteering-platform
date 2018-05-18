from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from ovp.apps.channels.exceptions import NoChannelSupplied

UserModel = get_user_model()

class ChannelBasedAuthentication(ModelBackend):
  def authenticate(self, request, username=None, password=None, channel=None, **kwargs):
    if username is None:
      username = kwargs.get(UserModel.USERNAME_FIELD)

    if channel is None:
      raise NoChannelSupplied()

    try:
      user = UserModel.objects.get(email=username, channel__slug=channel)
      user.LOGIN = True
    except UserModel.DoesNotExist:
      # Run the default password hasher once to reduce the timing
      # difference between an existing and a non-existing user (#20760).
      UserModel().set_password(password)
    else:
      if user.check_password(password) and self.user_can_authenticate(user):
        return user
