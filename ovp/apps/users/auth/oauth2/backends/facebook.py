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
    url = self.strategy.request.META['HTTP_HOST']
    print(url)
    with open('/home/ubuntu/teste.txt', 'w') as test:
      test.write(url)
    face_keys = json.loads(os.environ.get('FACEBOOK_KEYS', {}))
    for channel in face_keys:
      if channel in url:
        return tuple(face_keys[channel])
    return self.setting('KEY'), self.setting('SECRET')