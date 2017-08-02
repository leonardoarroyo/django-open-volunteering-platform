from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class Category(models.Model):
	name = models.CharField(_('name'), max_length=150, blank=False, null=False)
	slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
	description = models.CharField(_('description'), max_length=3000, blank=True, null=True)
	image = models.ForeignKey('uploads.UploadedImage', blank=True, null=True, verbose_name=_('image'), related_name="category_image")
	highlighted = models.BooleanField(_("Highlighted"), default=False, blank=False)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = self.generate_slug()

		return super(Category, self).save(*args, **kwargs)

	def generate_slug(self):
		if self.name:
			slug = slugify(self.name)[0:99]
			append = ''
			i = 0

			query = Category.objects.filter(slug=slug + append)
			while query.count() > 0:
				i += 1
				append = '-' + str(i)
				query = Category.objects.filter(slug=slug + append)
			return slug + append
		
		return None