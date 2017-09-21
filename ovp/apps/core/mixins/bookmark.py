from rest_framework import decorators
from rest_framework import response

class BookmarkMixin():
  """
  This mixin allows for easily addition of bookmarking to a model.
  Currently it is applied to projects and organizations.

  It allows for:
    - Bookmarking a model
    - Unbookmarking a model
    - Retrieving list of bookmarked objects
  """
  def bookmark(self, request, *args, **kwargs):
    pass

  def unbookmark(self, request, *args, **kwargs):
    pass

  def bookmarked(self, request, *args, **kwargs):
    pass
