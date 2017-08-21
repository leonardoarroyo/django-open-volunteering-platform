from django.db import models

class Comments(models.Model):
	project = models.ForeignKey('projects.Project', verbose_name=_('project'))
	content = models.TextField(_('content'), max_length=3000)
	user = models.ForeignKey('users.User', verbose_name=_('user'))
	reply_to = models.IntegerField(blank=False, null=False, default=0)
	created_date = models.DateTimeField(_('Created date'), auto_now_add=True)