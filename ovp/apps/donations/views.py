from django.shortcuts import get_object_or_404

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.donations.backends.zoop import ZoopBackend
from ovp.apps.donations.models import Transaction
from ovp.apps.organizations.models import Organization

from ovp.apps.donations.serializers import DonateSerializer
from ovp.apps.donations.serializers import TransactionRetrieveSerializer
from ovp.apps.donations.serializers import RefundTransactionSerializer

from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import response
from rest_framework import permissions

@ChannelViewSet
class DonationViewSet(viewsets.GenericViewSet):
  # POST /subscribe/
  # GET /subscriptions/
  # DELETE /subscription/

  def __init__(self, *args, **kwargs):
    self.backend = ZoopBackend()
    return super(DonationViewSet, self).__init__()

  def get_queryset(self, *args, **kwargs):
    if self.action in ["transactions", "refund_transaction"]:
      return Transaction.objects.filter(user=self.request.user).order_by("-pk")
    return None

  def get_serializer_class(self, *args, **kwargs):
    if self.action == "donate":
      return DonateSerializer
    if self.action == "transactions":
      return TransactionRetrieveSerializer
    if self.action == "refund_transaction":
      return RefundTransactionSerializer

  def get_permissions(self):
    if self.action == "donate":
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == "transactions":
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == "refund_transaction":
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
      object_channel=request.channel
    )

    return response.Response(charge_data[1], status=charge_data[0])

  @decorators.action(methods=["GET"], detail=False)
  def transactions(self, request):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return response.Response(serializer.data)

  @decorators.action(methods=["POST"], detail=False)
  def refund_transaction(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    queryset = self.filter_queryset(self.get_queryset())
    obj = get_object_or_404(queryset, uuid=serializer.data["uuid"], status="succeeded")

    status, backend_response = self.backend.refund_transaction(obj.backend_transaction_id, obj.amount)
    if status != 200:
      return response.Response({"success": False, "message": "Internal error ocurred."}, status=500)

    obj.status = backend_response.json()["status"]
    obj.save()

    return response.Response({"success": True, "status": "canceled"})

  @decorators.action(methods=["POST"], detail=False)
  def subscribe():
    pass

  @decorators.action(methods=["GET", "DELETE"], detail=False)
  def subscriptions():
    pass