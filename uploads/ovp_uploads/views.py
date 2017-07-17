import json

from ovp_uploads.models import UploadedImage
from ovp_uploads.serializers import UploadedImageSerializer, ImageGallerySerializer

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from .helpers import perform_image_crop


class UploadedImageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  queryset = UploadedImage.objects.all()
  serializer_class = UploadedImageSerializer

  def create(self, request, *args, **kwargs):
    upload_data = {}

    if request.data.get('image', None):
      upload_data['image'] = request.data.get('image')

    upload_header = request.META.get('HTTP_X_UNAUTHENTICATED_UPLOAD', None)
    is_authenticated = request.user.is_authenticated()

    if request.data.get('crop_rect', None):
      crop_rect = request.data.get('crop_rect')
      if isinstance(crop_rect, str):
        crop_rect = json.loads(crop_rect)
      upload_data['image'] = perform_image_crop(upload_data['image'], crop_rect)
      request.FILES['image'] = upload_data['image']

    if is_authenticated or upload_header:
      if upload_header:
        upload_data['user'] = None

      if is_authenticated:
        upload_data['user'] = request.user.id

      serializer = self.get_serializer(data=upload_data)

      if serializer.is_valid():
        self.object = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

      return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return response.Response(status=status.HTTP_401_UNAUTHORIZED)


class ImageGalleryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset = UploadedImage.objects.filter(category__isnull=False)
  serializer_class = ImageGallerySerializer

  def get_queryset(self):
    queryset = self.queryset
    category = self.request.query_params.get('category', None)
    if category is not None:
      queryset = queryset.filter(category=category)
    return queryset