from django.db import models
from django.utils.translation import ugettext_lazy as _
from redactor.fields import RedactorField

class Faq(models.Model):
	question = models.CharField(_('Pergunta'), max_length=100)
	answer = RedactorField(verbose_name=_('Resposta'), max_length=3000, default='')
	category = models.ForeignKey('faq.Category', verbose_name=_('Categoria'), null=False, blank=True, default=0)
