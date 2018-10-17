from django.conf.urls import url, include
from rest_framework import routers

from ovp.apps.ratings import views


router = routers.DefaultRouter()
router.register(r'ratings', views.RatingResourceViewSet, 'rating')

urlpatterns = [
  url(r'^', include(router.urls)),
]
