from social_core.backends.azuread import AzureADOAuth2 as AzureADOAuth2Base
from rest_framework.exceptions import AuthenticationFailed

class AzureADOAuth2(AzureADOAuth2Base):
  def auth_allowed(self, response, details):
    if not response.get("email", False):
      raise AuthenticationFailed({
        "error": "access_denied",
        "error_description": "Your email is not verified by the provider"
      })
    return super(AzureADOAuth2, self).auth_allowed(response, details)

  def get_user_details(self, response):
    data = super(AzureADOAuth2, self).get_user_details(response)
    return {
      'email': data['email'],
      'name': data['fullname'],
    }