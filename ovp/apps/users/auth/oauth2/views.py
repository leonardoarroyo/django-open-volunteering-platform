from rest_framework_social_oauth2.views import TokenView as BaseTokenView
from rest_framework_social_oauth2.oauth2_backends import KeepRequestCore
from .validators import OAuth2Validator
from .oauthlib_core import KeepRequestChannel

class TokenView(BaseTokenView):
  validator_class = OAuth2Validator
  oauthlib_backend_class = KeepRequestChannel
