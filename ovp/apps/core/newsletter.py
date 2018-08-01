from ovp.apps.core.emails import BaseMail

class Newsletter(BaseMail):
  """
  This class is responsible for firing newsletter for Users
  """
  def __init__(self, user):
    super(Newsletter, self).__init__(user.email, channel=user.channel.slug)
  
  def sendNewsletter(self, context={}):
    """
    Sent newsletter automatic
    """
    return self.sendEmail('newsletter', 'Newsletter do Mês', context)