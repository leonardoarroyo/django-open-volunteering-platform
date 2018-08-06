from django.core.management.base import BaseCommand

import requests

from ovp.apps.users.models import User
from ovp.apps.projects.models import Project, Category
from ovp.apps.search.filters import UserSkillsCausesFilter

class Command(BaseCommand):
  help = "Send newsletter automatic"
  def handle(self, *args, **options):

    context = {}
    context.setdefault('blog', {})
    context.setdefault('category', {})
    context.setdefault('highlight', None)
    context.setdefault('projects', [])

    highlight = Project.objects.filter(newsletter=True).order_by('-pk')
    context['highlight'] = highlight and highlight[0]

    blog = requests.get('https://blog.atados.com.br/wp-json/wp/v2/posts?per_page=1').json()
    context['blog'] = {
      'title': blog[0]['title']['rendered'], 
      'link': blog[0]['link']
    }

    category = Category.objects.filter(newsletter=True).order_by('-pk')
    if category:
      context['category'] = {
        'name': category[0].name,
        'projects': Project.objects.filter(categories=category[0])[:5]
      }
  
    for user in User.objects.all()[99:105]:
      context['projects'] = UserSkillsCausesFilter().annotate_queryset(Project.objects.all(), user)[:5]
      # Newsletter(user).sendNewsletter(context)
