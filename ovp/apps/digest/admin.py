from django.db import models
from martor.widgets import AdminMartorWidget
from ovp.apps.digest.models import DigestText
from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin

class DigestTextAdmin(ChannelModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    fields = [
        'text_content', 'keep_text'
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

admin_site.register(DigestText, DigestTextAdmin)
