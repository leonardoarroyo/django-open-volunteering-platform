from ovp.apps.channels.exceptions import UnexpectedMultipleChannelsAPIError

def ChannelViewSet(cls):
  """
  Wrapping any viewset with this decorator will make get_queryset result
  get filtered by channels set on the request header.

  Use for viewsets that handle a Channel resource.
  """
  # Patch queryset
  get_queryset = getattr(cls, "get_queryset", None)
  if get_queryset:
    def patched_get_queryset(self, *args, **kwargs):
      return get_queryset(self, *args, **kwargs).filter(channel__slug = self.request.channels[0])
    cls.get_queryset = patched_get_queryset

  # Channel amount verification
  initial = cls.initial
  def patched_initial(self, request, *args, **kwargs):
    if len(request.channels) != 1:
      raise UnexpectedMultipleChannelsAPIError()
    return initial(self, request, *args, **kwargs)
  cls.initial = patched_initial

  return cls
