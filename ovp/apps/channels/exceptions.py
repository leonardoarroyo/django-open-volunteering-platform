from rest_framework import status
from rest_framework.exceptions import APIException

class UnexpectedChannelAssociationError(Exception):
  def __init__(self):
    super(Exception, self).__init__("You can't associate a channel directly to single channel models. Pass object_channel to .save() or objects.create() method instead.")

class NoChannelSupplied(Exception):
  def __init__(self):
    super(Exception, self).__init__("A channel was expected but no channel was supplied.")
