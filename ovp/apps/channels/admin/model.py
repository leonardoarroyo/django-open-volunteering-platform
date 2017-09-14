from django.contrib.admin import ModelAdmin

class ChannelModelAdmin(ModelAdmin):
  def get_queryset(self, request):
    qs = super(ChannelModelAdmin, self).get_queryset(request)
    return qs.filter(channel=request.user.channel)
