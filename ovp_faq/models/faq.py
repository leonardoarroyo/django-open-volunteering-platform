from django.db import models
from django.utils.translation import ugettext_lazy as _
from redactor.fields import RedactorField

class Faq(models.Model):
	question = models.CharField(_('question'), max_length=100)
	answer = RedactorField(verbose_name=_('answer'), max_length=3000, default='')
	category = models.ForeignKey('ovp_faq.Category', verbose_name=_('category'), default=0)
