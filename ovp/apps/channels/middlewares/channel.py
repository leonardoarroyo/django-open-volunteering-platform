class ChannelMiddleware():
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    channels = request.META.get("HTTP_X_OVP_CHANNELS", "default")
    import pudb;pudb.set_trace()
    response = self.get_response(request)
    return response
