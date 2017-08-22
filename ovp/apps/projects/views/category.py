from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response
from rest_framework import decorators
from rest_framework import response

from ovp.apps.channels.viewsets.decorators import ChannelViewSet

from ovp.apps.projects import models
from ovp.apps.projects.serializers import category

@ChannelViewSet
class CategoryResourceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	# """
	# ProjectResourceViewSet resource endpoint
	# """
	queryset = models.Category.objects.all()

	def list(self, request):
		serializer = category.CategoryRetrieveSerializer(self.queryset, many=True)
		return response.Response(serializer.data)
