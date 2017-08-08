from rest_framework import routers

from django.conf.urls import url, include

from ovp.apps.channels.tests.helpers import views

test_user_resource = routers.SimpleRouter()
test_user_resource.register(r"test-users", views.ChannelUserTestViewSet, "test-users")

urlpatterns = [
  url(r"^", include(test_user_resource.urls)),
]
