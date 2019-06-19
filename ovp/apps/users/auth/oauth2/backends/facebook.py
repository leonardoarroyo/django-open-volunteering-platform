from social_core.backends.facebook import FacebookOAuth2 as FacebookOAuth2Base
from rest_framework.exceptions import AuthenticationFailed
import os
import json

class FacebookOAuth2(FacebookOAuth2Base):
  def auth_allowed(self, response, details):
    if not response.get("email", False):
      raise AuthenticationFailed({
        "error": "access_denied",
        "error_description": "Your email is not verified by the provider"
      })
    return super(FacebookOAuth2, self).auth_allowed(response, details)

  def get_user_details(self, response):
    data = super(FacebookOAuth2, self).get_user_details(response)
    return {
      'email': data['email'],
      'name': data['fullname'],
    }

  def get_key_and_secret(self):
    return os.environ['FACE_ID_TGS'], os.environ['FACE_SECRET_TGS']