from django.conf.urls import url, include
from rest_framework import routers

from ovp.apps.analytics import views

router = routers.DefaultRouter()
router.register(r'admin/analytics', views.AnalyticsResourceViewSet, 'analytics')

urlpatterns = [
  url(r'^', include(router.urls)),
]
