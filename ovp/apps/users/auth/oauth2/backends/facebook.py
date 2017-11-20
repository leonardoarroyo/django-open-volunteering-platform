from social_core.backends.facebook import FacebookOAuth2 as FacebookOAuth2Base
from rest_framework.exceptions import AuthenticationFailed

class FacebookOAuth2(FacebookOAuth2Base):
  def auth_allowed(self, response, details):
    if not response.get("verified", False):
      raise AuthenticationFailed({
        "error": "access_denied",
        "error_description": "Your email is not verified by the provider"
      })
    return super(FacebookOAuth2, self).auth_allowed(response, details)

  def get_user_details(self, response):
    data = super(FacebookOAuth2, self).get_user_details(response)
    return {
      'email': data['email'],
      'name': data['fullname']
    }
