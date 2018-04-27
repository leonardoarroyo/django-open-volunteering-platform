from django.core.exceptions import PermissionDenied

from ovp.apps.projects.serializers.project import ProjectSearchSerializer
from ovp.apps.projects.models import Project

from ovp.apps.organizations.models import Organization
from ovp.apps.organizations.serializers import OrganizationSearchSerializer

from ovp.apps.users.models.user import User
from ovp.apps.users.serializers.user import get_user_search_serializer
from ovp.apps.users.models.profile import get_profile_model, UserProfile

from ovp.apps.search import helpers
from ovp.apps.search import filters
from ovp.apps.search import querysets
from ovp.apps.search.decorators import cached

from ovp.apps.channels.cache import get_channel_setting

from django.core.cache import cache

from rest_framework import viewsets
from rest_framework import views
from rest_framework import mixins
from rest_framework import response
from rest_framework import decorators

from haystack.query import SearchQuerySet, SQ


class OrganizationSearchResource(mixins.ListModelMixin, viewsets.GenericViewSet):
  serializer_class = OrganizationSearchSerializer
  filter_backends = (filters.OrderingFilter,)
  ordering_fields = ('slug', 'name', 'website', 'facebook_page', 'details', 'description', 'type', 'hidden_address')

  def get_cache_key(self):
    if self.request.user.is_anonymous():
      return 'organizations-{}-{}'.format(self.request.channel, hash(frozenset(self.request.GET.items())))
    return None

  @cached
  def get_queryset(self):
    params = self.request.GET

    highlighted = params.get('highlighted') == 'true'
    published = params.get('published', 'true')

    query = params.get('query', None)
    cause = params.get('cause', None)
    address = params.get('address', None)
    name = params.get('name', None)

    queryset = SearchQuerySet().models(Organization)
    queryset = queryset.filter(highlighted=1) if highlighted else queryset
    queryset = queryset.filter(content=query) if query else queryset
    queryset = filters.by_name(queryset, name) if name else queryset
    queryset = filters.by_published(queryset, published)
    queryset = filters.by_address(queryset, address) if address else queryset
    queryset = filters.by_causes(queryset, cause) if cause else queryset
    queryset = queryset.filter(channel=self.request.channel)

    result_keys = [q.pk for q in queryset]
    result = querysets.get_organization_queryset(request=self.request).filter(pk__in=result_keys)
    result = filters.filter_out(result, "FILTER_OUT_ORGANIZATIONS", self.request.channel)

    return result


class ProjectSearchResource(mixins.ListModelMixin, viewsets.GenericViewSet):
  serializer_class = ProjectSearchSerializer
  filter_backends = (filters.ProjectRelevanceOrderingFilter,)
  ordering_fields = ('name', 'slug', 'details', 'description', 'highlighted', 'published_date', 'created_date', 'max_applies', 'minimum_age', 'hidden_address', 'crowdfunding', 'public_project', 'relevance')

  def get_cache_key(self):
    if self.request.user.is_anonymous():
      return 'projects-{}-{}'.format(self.request.channel, hash(frozenset(self.request.GET.items())))
    return None

  @cached
  def get_queryset(self):
    params = self.request.GET

    query = params.get('query', None)
    cause = params.get('cause', None)
    skill = params.get('skill', None)
    category = params.get('category', None)
    address = params.get('address', None)
    highlighted = (params.get('highlighted') == 'true')
    name = params.get('name', None)
    published = params.get('published', 'true')
    closed = params.get('closed', 'false')
    organization = params.get('organization', None)
    not_organization = params.get('not_organization', None)
    disponibility = params.get('disponibility', None)
    date = params.get('date', None)

    queryset = SearchQuerySet().models(Project)
    queryset = queryset.filter(highlighted=1) if highlighted else queryset
    queryset = queryset.filter(content=query) if query else queryset
    queryset = filters.by_published(queryset, published)
    queryset = filters.by_closed(queryset, closed)
    queryset = filters.by_address(queryset, address, project=True)
    queryset = filters.by_name(queryset, name)
    queryset = filters.by_skills(queryset, skill)
    queryset = filters.by_causes(queryset, cause)
    queryset = filters.by_categories(queryset, category)
    queryset = filters.by_disponibility(queryset, disponibility)
    queryset = filters.by_date(queryset, date)
    queryset = queryset.filter(channel=self.request.channel)

    result_keys = [q.pk for q in queryset]

    result = querysets.get_project_queryset(request=self.request).filter(pk__in=result_keys)

    if not_organization:
      org = [o for o in not_organization.split(',')]
      result = result.exclude(organization__in=org)
    elif organization:
      org = [o for o in organization.split(',')]
      result = result.filter(organization__in=org)

    result = filters.filter_out(result, "FILTER_OUT_PROJECTS", self.request.channel)

    return result


class UserSearchResource(mixins.ListModelMixin, viewsets.GenericViewSet):
  serializer_class = get_user_search_serializer()
  filter_backends = (filters.OrderingFilter,)
  ordering_fields = ('slug', 'name')

  def initialize_request(self, *args, **kwargs):
    request = super(UserSearchResource, self).initialize_request(*args, **kwargs)
    self.check_user_search_enabled(request.channel)
    return request

  def check_user_search_enabled(self, channel):
    if int(get_channel_setting(channel, "ENABLE_USER_SEARCH")[0]) == 0:
      raise PermissionDenied

  def get_cache_key(self):
    return 'users-{}-{}'.format(self.request.channel, hash(frozenset(self.request.GET.items())))

  @cached
  def get_queryset(self):
    params = self.request.GET

    cause = params.get('cause', None)
    skill = params.get('skill', None)
    name = params.get('name', None)

    queryset = SearchQuerySet().models(User)
    queryset = filters.by_skills(queryset, skill)
    queryset = filters.by_causes(queryset, cause)
    queryset = filters.by_name(queryset, name)
    queryset = queryset.filter(channel=self.request.channel)

    result_keys = [q.pk for q in queryset]
    related_field_name = get_profile_model()._meta.get_field('user').related_query_name()

    result = User.objects.order_by('-pk').filter(pk__in=result_keys, public=True).prefetch_related(related_field_name + '__skills', related_field_name + '__causes').select_related(related_field_name)

    return result

class CountryCities(views.APIView):
  def get(self, request, country):
    self.country = country
    result = self.get_country_cities(country)
    return response.Response(result)

  @cached
  def get_country_cities(self, country):
    result = {"projects": [], "organizations": [], "common": []}

    search_term = helpers.whoosh_raw("{}-country".format(country))

    queryset = SearchQuerySet().models(Project).filter(address_components__exact=search_term, published=1, closed=0, channel=self.request.channel)
    projects = helpers.get_cities(queryset)

    queryset = SearchQuerySet().models(Organization).filter(address_components__exact=search_term, published=1, channel=self.request.channel)
    organizations = helpers.get_cities(queryset)

    common = projects & organizations
    projects = projects - common
    organizations = organizations - common

    result["common"] = sorted(common)
    result["projects"] = sorted(projects)
    result["organizations"] = sorted(organizations)

    return result

  def get_cache_key(self):
    return "available-cities-{}-{}".format(self.request.channel, hash(self.country))
