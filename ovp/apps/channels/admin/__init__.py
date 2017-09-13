from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
#from .forms import ChannelAuthenticationForm

#site.login_form = ChannelAuthenticationForm

class ChannelAdminSite(AdminSite):
  site_header = 'Monty Python administration'

  @never_cache
  def login(self, request, channel_slug=None, extra_context=None):
    return super(ChannelAdminSite, self).login(request, extra_context)


admin_site = ChannelAdminSite(name='channeladmin')
