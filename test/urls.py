from django.conf.urls import url, include

import ovp.apps.core.urls
import ovp.apps.uploads.urls
import ovp.apps.users.urls
import ovp.apps.projects.urls
import ovp.apps.organizations.urls
import ovp.apps.search.urls
import ovp.apps.faq.urls
import ovp.apps.faq.urls

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

  # Search
  url(r'^', include(ovp.apps.search.urls)),

  # FAQ
  url(r'^', include(ovp.apps.faq.urls)),

]

# Test urls
# These should not be used in production
import ovp.apps.channels.tests.helpers.urls
urlpatterns += [
  url(r'^', include(ovp.apps.channels.tests.helpers.urls))
]
