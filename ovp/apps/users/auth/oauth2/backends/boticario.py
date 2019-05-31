from social_core.backends.oauth import BaseOAuth2
from rest_framework.exceptions import AuthenticationFailed

class BoticarioOAuth2(BaseOAuth2):
    """Boticario OAuth2 authentication backend"""
    name = "boticario"
    AUTHORIZATION_URL = "https://auth.grupoboticario.com.br/adfs/oauth2/authorize/"
    ACCESS_TOKEN_URL = "https://auth.grupoboticario.com.br/adfs/oauth2/token/"
    REVOKE_TOKEN_URL = "https://auth.grupoboticario.com.br/adfs/oauth2/logout"
    DEFAULT_SCOPE = ['openid', 'email', 'profile']

    def auth_allowed(self, response, details):
        if not response.get("email", False):
            raise AuthenticationFailed({
                "error": "access_denied",
                "error_description": "Your email is not verified by the provider"
            })
        return super(BoticarioOAuth2, self).auth_allowed(response, details)

    def get_user_details(self, response):
        return {
            'email': response.get('email'),
            'name': response.get('fullname')
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            "https://auth.grupoboticario.com.br/adfs/userinfo",
            headers={
                'Authorization': 'Bearer {}'.format(access_token),
            },
)