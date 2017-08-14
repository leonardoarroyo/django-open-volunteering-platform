from django.conf.urls import url, include
from rest_framework import routers
from ovp.apps.users import views
from ovp.apps.users.auth.jwt import obtain_jwt_token

router = routers.SimpleRouter()
router.register(r'users', views.UserResourceViewSet, 'user')
router.register(r'users/recovery-token', views.RecoveryTokenViewSet, 'recovery-token')
router.register(r'users/recover-password', views.RecoverPasswordViewSet, 'recover-password')
router.register(r'public-users', views.PublicUserResourceViewSet, 'public-users')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^api-token-auth/', obtain_jwt_token, name='api-token-auth'),
]
