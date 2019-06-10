from social_core.backends.oauth import BaseOAuth2
from rest_framework.exceptions import AuthenticationFailed

import jwt
import os
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

aud = "e7caf061-061a-4047-97e1-4fca75474527"

def load_certificate_content():
  path = os.environ.get("AUTH_CERT_PATH")
  with open(path, "r") as f:
    return f.read()

def verify_and_decode_token(token):
  cert_content = load_certificate_content()
  cert_obj = load_pem_x509_certificate(cert_content.encode('ascii'), default_backend())
  public_key = cert_obj.public_key()
  try:
    decoded = jwt.decode(token, public_key, algorithms=['RS256'], audience=aud)
    return decoded
  except jwt.exceptions.InvalidSignatureError:
    return None

class BoticarioOAuth2(BaseOAuth2):
  """Boticario OAuth2 authentication backend"""
  name = "boticario"

  def __init__(self, *args, **kwargs):
    super(BoticarioOAuth2, self).__init__(*args, **kwargs)

  def get_json(self, *args, **kwargs):
    return None

  def auth_allowed(self, response, details):
    # We just make sure there's token data
    # At this point the token signature has already been checked so we can trust it
    if response.get('email', None):
      return True
    return False

  def get_user_details(self, response):
    return {
      'email': response.get('email'),
      'name': response.get('unique_name'),
    }

  def get_user_id(self, details, response):
    return details['email']

  def user_data(self, access_token, *args, **kwargs):
    self.token_data = verify_and_decode_token(access_token)
    return self.token_data
