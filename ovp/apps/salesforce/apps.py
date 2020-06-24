from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SalesforceConfig(AppConfig):
    name = 'ovp.apps.salesforce'
    verbose_name = _('Users')

    def ready(self):
        from . import signals
