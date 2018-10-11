from rest_framework import response
from rest_framework.decorators import detail_route
from drf_yasg.utils import swagger_auto_schema

class CommentaryCreateMixin:
  @swagger_auto_schema(method="POST", responses={200: "OK"})
  @detail_route(['POST'], url_path='commentary')
  def commentary(self, request, slug, pk=None):
    """ Create an commentary for an object. """
    data = request.data
    user = request.user
    obj = self.get_object()

    data['user'] = user.pk

    serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    obj.commentaries.add(serializer.instance)
    obj.save()

    return response.Response(serializer.data)
