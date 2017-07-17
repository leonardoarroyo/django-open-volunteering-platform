from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
	name = models.CharField(_('Category name'), max_length=100)

	def __str__(self):
		return self.name