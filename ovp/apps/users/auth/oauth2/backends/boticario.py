from social_core.backends.oauth import BaseOAuth2
from rest_framework.exceptions import AuthenticationFailed

import jwt
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

aud = "e7caf061-061a-4047-97e1-4fca75474527"
certificate = "-----BEGIN CERTIFICATE-----\nMIIC8DCCAdigAwIBAgIQGAFIK59KvZtK2u/9iEkBqTANBgkqhkiG9w0BAQsFADA0MTIwMAYDVQQDEylBREZTIFNpZ25pbmcgLSBhdXRoLmdydXBvYm90aWNhcmlvLmNvbS5icjAeFw0xODAxMDkxNDI1MDNaFw0yODAxMDcxNDI1MDNaMDQxMjAwBgNVBAMTKUFERlMgU2lnbmluZyAtIGF1dGguZ3J1cG9ib3RpY2FyaW8uY29tLmJyMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyKzTouKEls7vp839l8OX/Ns07qikR5E8v4d3ml1n5jam9V4nLNUDC3MGKH1pYTI4qT6HdHnuHHgF3lMOVO3Rjr4ql5QXsR4qGS3qwUTT7S/mDgOlP5fFAFZxkgpqOlu+xDFSCv6vJRx2kezflWtehyo1Sr4Bu4CeohxpUntLyD6XJlwhwLaSdMl3A6T3MEDWVabfpbVSQ4J33jTeek3DAGRC6a9TIjELVOO4whSN9eSWdhP3wtHEW323im5wGwUnnRAU9yKSCxmfSRJFO4M7VL0aJOIJjUCumq4OMOx1/x4hw4M0Vf0oUtNVySn0DtriBydYVCy/Cr8JtnIYvglqpQIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQAcVQZbnedv1fp9FeHVhWwNwv6CUC+KF8MevI76MYxlZnwkF1albH1FJORRJoiMsCyRwEP6z8Y/Scs2fqP920zXy07coImh4SSaoWMo7QGWoFEDgh3/J5lh9d7o26aTz2RH0SVQz21uwCUKmqbDY0wSH0KLTMnDLej8N/L4hpj5wlFwH+VX8iKN8WQWRFj3zUiKPNkU48cBDvAP4twQSroXtkZfEnqTBjfrdW7Aj31qB93j9rNb+TV1cB2th82Ui0ima3Cmwuo3++QMHVDLWjH0CWpR7FIYXoXM1omPDYb0M3O1jJZ7LF8U/in/9CdKdTMaxZg7PAxvNT7jvFEuBHkM\n-----END CERTIFICATE-----"

def verify_and_decode_token(token):
  cert_obj = load_pem_x509_certificate(certificate.encode('ascii'), default_backend())
  public_key = cert_obj.public_key()
  try:
    return jwt.decode(token, public_key, algorithms=['RS256'], audience=aud)
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
      'email': response.get('email', ''),
      'name': response.get('unique_name', ''),
    }

  def user_data(self, access_token, *args, **kwargs):
    self.token_data = verify_and_decode_token(access_token)
    return self.token_data
