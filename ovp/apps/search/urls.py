from django.conf.urls import url, include
from rest_framework import routers
from ovp.apps.search import views


project_search = routers.SimpleRouter()
project_search.register(r'projects', views.ProjectSearchResource, 'search-projects')

organization_search = routers.SimpleRouter()
organization_search.register(r'organizations', views.OrganizationSearchResource, 'search-organizations')

user_search = routers.SimpleRouter()
user_search.register(r'users', views.UserSearchResource, 'search-users')

urlpatterns = [
  url(r'^search/', include(project_search.urls)),
  url(r'^search/', include(organization_search.urls)),
  url(r'^search/', include(user_search.urls)),
  url(r'^search/available-cities/(?P<country>[^/]+)/', views.available_country_cities, name='available-country-cities'),
]
