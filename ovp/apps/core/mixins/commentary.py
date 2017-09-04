from rest_framework import decorators
from rest_framework import response

class CommentaryCreateMixin:
  @decorators.detail_route(['POST'], url_path='commentary')
  def commentary(self, request, slug, pk=None):
    data = request.data
    user = request.user
    obj = self.get_object()

    commentaries = []
    c = obj.commentaries.all()
    for x in c:
      commentaries.append(x)

    data['user'] = user.pk

    serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    commentaries.append(serializer.instance)
    obj.commentaries = commentaries
    obj.save()

    return response.Response(serializer.data)
    