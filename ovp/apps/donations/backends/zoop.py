import requests
from django.conf import settings

POST="post"
GET="get"
PATCH="patch"
PUT="put"
DELETE="delete"

class ZoopBackend():
  def __init__(self):
    self.marketplace_id = getattr(settings, "ZOOP_MARKETPLACE_ID", None)
    self.pub_key = getattr(settings, "ZOOP_PUB_KEY", None)
    assert self.marketplace_id and self.pub_key

  def _build_url(self, resource):
    return "https://api.zoop.ws/" + resource.format(mpid=self.marketplace_id)

  def call(self, http_method, resource, data):
    call_method = getattr(requests, http_method)
    url = self._build_url(resource)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return call_method(url, json=data, auth=(self.pub_key, ''), headers=headers)

  def generate_card_token(self,
                          holder_name=None,
                          expiration_month=None,
                          expiration_year=None,
                          security_code=None,
                          card_number=None):
    data = {
      "holder_name": holder_name,
      "expiration_month": expiration_month,
      "expiration_year": expiration_year,
      "security_code": security_code,
      "card_number": card_number
    }
    return self.call(POST, "v1/marketplaces/{mpid}/cards/tokens", data)

  def charge(self, token):
    data = {
      "payment_type": "credit",
      "amount": 100,
      "on_behalf_of": "33aec500d6094db0a6367103a0645d32",
      "source": {
        "usage": "single_use",
        "capture": True,
        "currency": "BRL",
        "type": "token",
        "token": {
          "id": token
        }
      }
    }
    data = {
      "payment_type": "credit",
      "currency": "BRL",
      "description": "donation",
      "amount": 100,
      "on_behalf_of": "33aec500d6094db0a6367103a0645d32",
      "statement_descriptor": "Atados",
      "token": token
    }
    return self.call(POST, "v1/marketplaces/{mpid}/transactions", data)