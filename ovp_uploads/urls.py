from django.conf.urls import url, include
from rest_framework import routers

from ovp_uploads import views

router = routers.DefaultRouter()
router.register(r'uploads/images', views.UploadedImageViewSet, 'upload-images')
router.register(r'image-gallery', views.ImageGalleryViewSet, 'image-gallery')

urlpatterns = [
  url(r'^', include(router.urls)),
]
