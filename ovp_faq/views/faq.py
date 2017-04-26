from ovp_faq.models.faq import Faq
from ovp_faq.serializers.faq import Faq as faq_serializer

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import response

class FaqResourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
  FaqResourceViewSet resource endpoint
  """
	queryset = Faq.objects.all()

	def list(self, request):
		params = self.request.GET
		category = params.get('category', None)
		
		self.queryset = self.queryset.filter(category=category)
		serializer = faq_serializer(self.queryset, many=True)

		return response.Response(serializer.data)

	def get_serializer_class(self):
		if self.action == 'list':
			return faq_serializer