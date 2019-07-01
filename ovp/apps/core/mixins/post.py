from rest_framework import response
from rest_framework.decorators import detail_route
from drf_yasg.utils import swagger_auto_schema

class PostCreateMixin:
  @swagger_auto_schema(method="POST", responses={200: "OK"})
  @detail_route(['POST'], url_path='post')
  def post(self, request, slug, pk=None):
    """ Create a post for an object. """
    data = request.data
    user = request.user
    obj = self.get_object()

    data['user'] = user.pk

    serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    obj.posts.add(serializer.instance)
    obj.save()

    return response.Response(serializer.data)
