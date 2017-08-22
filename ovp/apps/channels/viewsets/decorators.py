def ChannelViewSet(cls):
  """
  Wrapping any viewset with this decorator will make get_queryset result
  get filtered by channel set on the request header.

  Use for viewsets that handle a Channel resource.
  """
  # Patch queryset
  get_queryset = getattr(cls, "get_queryset", None)
  if get_queryset:
    def patched_get_queryset(self, *args, **kwargs):
      return get_queryset(self, *args, **kwargs).filter(channel__slug = self.request.channel)
    cls.get_queryset = patched_get_queryset

  return cls
