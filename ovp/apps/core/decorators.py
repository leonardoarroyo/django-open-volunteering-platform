from functools import wraps

def add_is_bookmarked_representation(func):
  """ Used to decorate Serializer.to_representation method.
      It sets the field "is_bookmarked" if the user has bookmarked the object
  """
  @wraps(func)
  def _impl(self, instance):
    ret = func(self, instance)

    user = self.context["request"].user
    bookmarked = False
    if not user.is_anonymous():
      bookmarked = instance.is_bookmarked(user)

    ret["is_bookmarked"] = bookmarked

    return ret
  return _impl
