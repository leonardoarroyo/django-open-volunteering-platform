from django.conf.urls import url, include

import ovp.apps.core.urls
import ovp.apps.uploads.urls
import ovp.apps.users.urls
import ovp.apps.projects.urls
import ovp.apps.organizations.urls

urlpatterns = [
  # Core
  url(r'^', include(ovp.apps.core.urls)),

  # Uploads
  url(r'^', include(ovp.apps.uploads.urls)),

  # Users
  url(r'^', include(ovp.apps.users.urls)),

  # Projects
  url(r'^', include(ovp.apps.projects.urls)),

  # Organizations
  url(r'^', include(ovp.apps.organizations.urls)),
]
