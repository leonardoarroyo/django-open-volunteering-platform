from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import permissions

class BookmarkMixin():
  """
  This mixin allows for easily addition of bookmarking to a model.
  Currently it is applied to projects and organizations.

  It allows for:
    - Bookmarking a model
    - Unbookmarking a model
    - Retrieving list of bookmarked objects

  To use this mixin on your viewset it must declare two methods.
  .get_bookmark_model which returns a bookmark model which has an user
  foreign key and a related model foreign key.
  .get_bookmark_kwargs which returns a dictionary with data to create
  and filter a given bookmark. Usually it contains an instance to the
  related bookmark model.

  Such model may look something like this:
    class ProjectBookmark(models.Model):
      user = models.ForeignKey('User')
      project = models.ForeignKey('Project')

  And the methods like:
    def get_bookmark_model(self):
      return ProjectBookmark

    def get_bookmark_kwargs(self):
      return {"project": self.get_object()}

  You also need to return the correct serializer for 'bookmarked' action
  on .get_serializer_class, as well as set self.permissions_classes =
  super().get_bookmark_permissions() for actions ['bookmark', 'unbookmark', 'bookmarked']

  """
  @decorators.detail_route(["POST"])
  def bookmark(self, request, *args, **kwargs):
    if self.get_bookmark_object():
      return response.Response({"detail": "Can't bookmark an object that has been already bookmarked.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

    bookmark = self.get_bookmark_model()(user=request.user, **self.get_bookmark_kwargs())
    bookmark.save(object_channel=request.channel)

    return response.Response({"detail": "Object sucesfully bookmarked.", "success": True})

  @decorators.detail_route(["POST"])
  def unbookmark(self, request, *args, **kwargs):
    bookmark = self.get_bookmark_object()
    if not bookmark:
      return response.Response({"detail": "Can't unbookmark an object that it not bookmarked.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

    bookmark.delete()

    return response.Response({"detail": "Object sucesfully unbookmarked.", "success": True})

  @decorators.list_route(["GET"])
  def bookmarked(self, request, *args, **kwargs):
    queryset = self.get_queryset().filter(projectbookmark__user=request.user, projectbookmark__channel__slug=request.channel)

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def get_bookmark_object(self):
    Bookmark = self.get_bookmark_model()
    bookmark_kwargs = self.get_bookmark_kwargs()

    try:
      return Bookmark.objects.get(user=self.request.user, channel__slug=self.request.channel, **bookmark_kwargs)
    except Bookmark.DoesNotExist:
      return None

  def get_bookmark_permissions(self):
    return (permissions.IsAuthenticated, )

  def get_bookmark_model(self):
    raise NotImplemented("Your viewset must override .get_bookmark_model")

  def get_bookmark_kwargs(self):
    raise NotImplemented("Your viewset must override .get_bookmark_kwargs")
