from rest_framework.serializers import Serializer
from rest_framework.fields import IntegerField
from ovp.apps.core.models import Skill
from ovp.apps.core.models import Cause
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from .skill import SkillSerializer
from .cause import FullCauseSerializer

class StartupData():
  def __init__(self, request):
    self.skills = Skill.objects.filter(channel__slug=request.channel)
    self.causes = Cause.objects.filter(channel__slug=request.channel)
    self.volunteer_count = User.objects.filter(channel__slug=request.channel).count()
    self.nonprofit_count = Organization.objects.filter(channel__slug=request.channel, published=True).count()

class StartupSerializer(Serializer):
  skills = SkillSerializer(many=True, required=False)
  causes = FullCauseSerializer(many=True, required=False)
  volunteer_count = IntegerField(required=False)
  nonprofit_count = IntegerField(required=False)