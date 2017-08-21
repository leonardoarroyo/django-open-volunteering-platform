from rest_framework import status
from rest_framework.exceptions import APIException

class UnexpectedMultipleChannelsError(Exception):
  def __init__(self):
    super(Exception, self).__init__("You have passed multiple channels down to a single channel resource.")

class UnexpectedChannelAssociationError(Exception):
  def __init__(self):
    super(Exception, self).__init__("You can't associate a channel directly to single channel models. Pass object_channels to .save() or objects.create() method instead.")

class NoChannelSupplied(Exception):
  def __init__(self):
    super(Exception, self).__init__("A channel was expected but no channel was supplied.")

class UnexpectedMultipleChannelsAPIError(APIException):
  status_code = status.HTTP_400_BAD_REQUEST
  default_detail = 'This is a single channel resource. You must specify only one channel in your request.'
  default_code = 'invalid'
