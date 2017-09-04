from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp.apps.projects.emails import CommentsEmail

class Commentary(models.Model):
	content = models.TextField(_('content'), max_length=3000)
	user = models.ForeignKey('users.User', verbose_name=_('user'))
	reply_to = models.ForeignKey('Commentary', verbose_name=_('reply'), blank=True, null=True)
	created_date = models.DateTimeField(_('Created date'), auto_now_add=True)

	def mailing(self, async_mail=None):
		return CommentsEmail(self, async_mail)

	def save(self, *args, **kwargs):
		if self.reply_to:
			self.mailing().sendReplyComment({"user": self.user, "content": self.content})
		else:
			self.mailing().sendComment({"user": self.user, "content": self.content})
		
		return super(Commentary, self).save(*args, **kwargs)
