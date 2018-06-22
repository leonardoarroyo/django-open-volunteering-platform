from rest_framework import response
from rest_framework import decorators
from rest_framework import status

from ovp.apps.core import models
from ovp.apps.core import serializers
from ovp.apps.core import emails

from django.utils import translation

@decorators.api_view(["GET"])
def startup(request):
  """ This view provides initial data to the client, such as available skills and causes """
  with translation.override(translation.get_language_from_request(request)):
    skills = serializers.SkillSerializer(models.Skill.objects.filter(channel__slug=request.channel), many=True)
    causes = serializers.FullCauseSerializer(models.Cause.objects.filter(channel__slug=request.channel), many=True, context={'request': request})

    return response.Response({
      "skills": skills.data,
      "causes": causes.data
    })

@decorators.api_view(["POST"])
def contact(request):
  name = request.data.get("name", "")
  message = request.data.get("message", "")
  email = request.data.get("email", "")
  phone = request.data.get("phone", "")
  recipients = request.data.get("recipients", request.data.get("recipients[]", []))
  context = {"name": name, "message": message, "email": email, "phone": phone}

  if not type(recipients) is list:
    recipients = [recipients]

  # Check if all recipients are valid
  contacts = models.ChannelContact.objects.filter(email__in=recipients, channel__slug=request.channel)
  if contacts.count() != len(recipients):
    return response.Response({"detail": "Invalid recipients."}, status.HTTP_400_BAD_REQUEST)

  contact = emails.ContactFormMail(recipients, channel=request.channel)
  contact.sendContact(context=context)

  return response.Response({"success": True})

@decorators.api_view(["POST"])
def record_lead(request):
  models.Lead.objects.create(
    name=request.data.get('name', None),
    email=request.data.get('email', None),
    phone=request.data.get('phone', None),
    country=request.data.get('country', None),
    city=request.data.get('city', None),
    object_channel=request.channel
  )
  return response.Response({"success": True})
