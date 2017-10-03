from rest_framework import views
from rest_framework import response

from ovp.apps.projects.serializers.project import ProjectSearchSerializer

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from ovp.apps.catalogue.cache import get_catalogue
from ovp.apps.catalogue.cache import fetch_catalogue

@ChannelViewSet
class CatalogueView(views.APIView):
  def get(self, request, slug):
    catalogue = get_catalogue(request.channel, slug)
    if not catalogue:
      return response.Response({"detail": "This catalog does not exist"}, status=404)

    fetched = fetch_catalogue(catalogue, serializer=ProjectSearchSerializer, request=self.request)

    return response.Response(fetched)
