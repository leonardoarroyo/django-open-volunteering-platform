from django.conf.urls import url, include

import ovp.apps.core.urls

urlpatterns = [
  url(r'^', include(ovp.apps.core.urls)),
]
