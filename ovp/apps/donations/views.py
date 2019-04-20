from rest_framework import viewsets
from rest_framework import decorators

class DonationViewSet(viewsets.GenericViewSet):
  # POST /donate/
  # POST /subscribe/
  # GET /transactions/
  # GET /subscriptions/
  # DELETE /subscription/

  @decorators.action(methods=["POST"], detail=False)
  def donate():
    pass

  @decorators.action(methods=["POST"], detail=False)
  def subscribe():
    pass

  @decorators.action(methods=["GET"], detail=False)
  def transactions():
    pass

  @decorators.action(methods=["GET", "DELETE"], detail=False)
  def subscriptions():
    pass