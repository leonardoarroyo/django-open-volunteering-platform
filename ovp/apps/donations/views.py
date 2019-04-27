from ovp.apps.donations.serializers import DonateSerializer
from ovp.apps.donations.backends.zoop import ZoopBackend
from ovp.apps.donations.models import Transaction
from ovp.apps.organizations.models import Organization

from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import response
from rest_framework import permissions

class DonationViewSet(viewsets.GenericViewSet):
  # POST /donate/
  # POST /subscribe/
  # GET /transactions/
  # GET /subscriptions/
  # DELETE /subscription/

  def __init__(self, *args, **kwargs):
    self.backend = ZoopBackend()
    return super(DonationViewSet, self).__init__()

  def get_queryset(self, *args, **kwargs):
    return None

  def get_serializer_class(self, *args, **kwargs):
    if self.action == "donate":
      return DonateSerializer

  def get_permissions(self):
    if self.action == "donate":
      self.permission_classes = (permissions.IsAuthenticated,)
    return super(DonationViewSet, self).get_permissions()

  ##################
  # ViewSet routes #
  ##################
  @decorators.action(methods=["POST"], detail=False)
  def donate(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    charge_data = self.backend.charge(token=data["token"], amount=data["amount"])
    backend_response_data = charge_data[2].json()

    Transaction.objects.create(
      user=self.request.user,
      organization=Organization.objects.get(pk=data["organization_id"]),
      amount=data["amount"],
      used_token=data["token"],
      status=charge_data[1]["status"],
      message=charge_data[1]["message"],
      backend_transaction_id=backend_response_data.get("id", None),
      backend_transaction_number=backend_response_data.get("transaction_number", None),
    )

    return response.Response(charge_data[1], status=charge_data[0])

  @decorators.action(methods=["POST"], detail=False)
  def subscribe():
    pass

  @decorators.action(methods=["GET"], detail=False)
  def transactions():
    pass

  @decorators.action(methods=["GET", "DELETE"], detail=False)
  def subscriptions():
    pass