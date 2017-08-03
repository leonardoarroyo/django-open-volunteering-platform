class ChannelMiddleware():
  def __init__(self, get_response):
    self.get_response = get_response

  def add_channels(self, request):
    self.channels = [x.strip() for x in request.META.get("HTTP_X_OVP_CHANNELS", "default").split(";")]
    request.channels = self.channels
    return request

  def __call__(self, request):
    # Parse and add channels
    request = self.add_channels(request)

    # Process request
    response = self.get_response(request)

    # Add channels header to response
    response["X-OVP-Channels"] = ";".join(self.channels)
    return response
