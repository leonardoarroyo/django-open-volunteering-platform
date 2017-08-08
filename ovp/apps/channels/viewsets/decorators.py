def ChannelViewSet(cls):
  """ Wrapping any viewset with this decorator will make get_queryset result
  get filtered by channels set on the request header
  """
  get_queryset = cls.get_queryset

  def func(self, *args, **kwargs):
    return get_queryset(self, *args, **kwargs).filter(channels__slug__in = self.request.channels).distinct()

  cls.get_queryset = func

  return cls
