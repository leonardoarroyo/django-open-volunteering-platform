from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from ovp.apps.users import models
from ovp.apps.users.helpers import get_settings, import_from_string
from ovp.apps.users.models.profile import get_profile_model
from ovp.apps.users.serializers.profile import get_profile_serializers
from ovp.apps.users.serializers.profile import ProfileSearchSerializer
from ovp.apps.users.validators import PasswordReuse
from ovp.apps.users.decorators import expired_password
from ovp.apps.organizations.serializers import OrganizationSearchSerializer, OrganizationOwnerRetrieveSerializer

from ovp.apps.projects.serializers.apply_user import ApplyUserRetrieveSerializer
from ovp.apps.projects import models as model_project

from ovp.apps.uploads.serializers import UploadedImageSerializer

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields

class UserCreateSerializer(ChannelRelationshipSerializer):
  profile = get_profile_serializers()[0](required=False)
  slug = serializers.CharField(read_only=True)
  uuid = serializers.CharField(read_only=True)

  class Meta:
    model = models.User
    fields = ['uuid', 'name', 'email', 'password', 'phone', 'avatar', 'locale', 'profile', 'public', 'slug', 'is_subscribed_to_newsletter']
    extra_kwargs = {'password': {'write_only': True}}

  def validate(self, data):
    errors = dict()

    if data.get('password'):
      password = data.get('password', '')
      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

    if data.get('email'):
      email = data.get('email', '')
      users = models.User.objects.filter(email=email, channel__slug=self.context["request"].channel)
      if users.count():
        errors['email'] = "An user with this email is already registered."

    if errors:
      raise serializers.ValidationError(errors)

    return super(UserCreateSerializer, self).validate(data)

  def create(self, validated_data):
    profile_data = validated_data.pop('profile', {})

    # Create user
    user = super(UserCreateSerializer, self).create(validated_data)

    # Profile
    profile_data['user'] = user
    profile_sr = get_profile_serializers()[0](data=profile_data, context=self.context)
    profile = profile_sr.create(profile_data)

    return user

class UserUpdateSerializer(UserCreateSerializer):
  password = fields.CharField(write_only=True, validators=[PasswordReuse()])
  current_password = fields.CharField(write_only=True)
  profile = get_profile_serializers()[0](required=False)

  class Meta:
    model = models.User
    permission_classes = (permissions.IsAuthenticated,)
    fields = ['name', 'phone', 'password', 'avatar', 'current_password', 'locale', 'profile', 'public', 'is_subscribed_to_newsletter']
    extra_kwargs = {'password': {'write_only': True}}


  def validate(self, data):
    errors = dict()

    if data.get('password') or data.get('current_password'):
      current_password = data.pop('current_password', '')
      password = data.get('password', '')

      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

      if not authenticate(email=self.context['request'].user.email, password=current_password, channel=self.context["request"].channel):
        errors['current_password'] = ["Invalid password."]

    if errors:
      raise serializers.ValidationError(errors)

    return super(UserCreateSerializer, self).validate(data)

  def update(self, instance, data):
    ProfileModel = get_profile_model()
    profile_data = data.pop('profile', None)

    if profile_data:
      has_profile=False
      try:
        if instance.profile:
          has_profile=True
        else:
          has_profile=False
      except models.UserProfile.DoesNotExist:
        has_profile=False

      if has_profile:
        profile = instance.profile
      else:
        profile = ProfileModel(user=instance)
        profile.save(object_channel=self.context["request"].channel)

      profile_sr = get_profile_serializers()[0](profile, data=profile_data, partial=True)
      profile_sr.is_valid(raise_exception=True)
      profile = profile_sr.update(profile, profile_sr.validated_data)

    return super(UserUpdateSerializer, self).update(instance, data)


class CurrentUserSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()
  profile = get_profile_serializers()[1]()
  organizations = OrganizationOwnerRetrieveSerializer(many=True)

  class Meta:
    model = models.User
    fields = ['uuid', 'name', 'phone', 'avatar', 'email', 'locale', 'profile', 'slug', 'public', 'organizations', 'is_subscribed_to_newsletter']

  @expired_password
  def to_representation(self, *args, **kwargs):
    return super(CurrentUserSerializer, self).to_representation(*args, **kwargs)

class ShortUserPublicRetrieveSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['uuid', 'name', 'avatar', 'slug']

class LongUserPublicRetrieveSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()
  profile = get_profile_serializers()[1]()
  applies = ApplyUserRetrieveSerializer(many=True, source="apply_set")

  class Meta:
    model = models.User
    fields = ['name', 'avatar', 'profile', 'slug', 'applies']

class UserProjectRetrieveSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['uuid', 'name', 'avatar', 'email', 'phone', 'slug']

class UserApplyRetrieveSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['uuid', 'name', 'avatar', 'phone', 'email']

class UserSearchSerializer(ChannelRelationshipSerializer):
  avatar = UploadedImageSerializer()
  profile = get_profile_serializers()[2]()

  class Meta:
    model = models.User
    fields = ['slug', 'name', 'avatar', 'profile']

def get_user_search_serializer():
  s = get_settings()
  class_path = s.get('USER_SEARCH_SERIALIZER', None)
  if class_path:
    return import_from_string(class_path)
  return UserSearchSerializer
