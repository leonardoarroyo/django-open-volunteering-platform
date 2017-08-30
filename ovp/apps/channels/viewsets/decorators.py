def ChannelViewSet(cls):
  """
  Wrapping any viewset with this decorator will make get_queryset result
  get filtered by channel set on the request header.

  Use for viewsets that handle a Channel resource.
  """
  # Patch get queryset
  get_queryset = getattr(cls, "get_queryset", None)
  if get_queryset:
    def patched_get_queryset(self, *args, **kwargs):
      return get_queryset(self, *args, **kwargs).filter(channel__slug = self.request.channel)
    cls.get_queryset = patched_get_queryset

  # We also patch the queryset
  queryset = getattr(cls, "queryset", None)
  if queryset is not None:
    @property
    def patched_queryset(self):
      return queryset.filter(channel__slug = self.request.channel)
    cls.queryset = patched_queryset

  # If get_queryset calls self.queryset, there's no problem filtering twice
  # as django evaluates queries lazily

  return cls
