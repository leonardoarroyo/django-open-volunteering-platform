from django.conf.urls import url, include

import ovp.apps.core.urls
import ovp.apps.uploads.urls

urlpatterns = [
  # Core
  url(r'^', include(ovp.apps.core.urls)),

  # Uploads
  url(r'^', include(ovp.apps.uploads.urls)),
]
