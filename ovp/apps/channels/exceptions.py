class UnexpectedMultipleChannelsError(Exception):
  def __init__(self):
    super(Exception, self).__init__("You have passed multiple channels down to a single channel resource.")

class UnexpectedChannelAssociationError(Exception):
  def __init__(self):
    super(Exception, self).__init__("You can't associate a channel directly to single channel models. Pass object_channels to .save() or objects.create() method instead.")
