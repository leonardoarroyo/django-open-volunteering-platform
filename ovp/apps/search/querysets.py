from ovp.apps.core.helpers.bookmark import annotate_bookmark

from ovp.apps.projects.models import Project
from ovp.apps.organizations.models import Organization
from ovp.apps.users.models.user import User


def get_organization_queryset(request=None):
    queryset = Organization.objects.filter(deleted=False) \
        .prefetch_related('causes', 'causes__image') \
        .select_related('address', 'channel', 'image') \
        .order_by('-highlighted')
    queryset = annotate_bookmark(queryset, request=request)
    return queryset


def get_project_queryset(request=None):
    queryset = Project.objects \
        .prefetch_related('skills', 'causes', 'categories', 'job__dates', 'causes__image') \
        .select_related('address', 'organization__address', 'owner', 'work', 'job', 'channel', 'organization', 'image',  'organization__image') \
        .filter(deleted=False) \
        .order_by('-pk')
    queryset = annotate_bookmark(queryset, request=request)
    return queryset
