from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _

def ChannelAuthenticationForm(AuthenticationForm):
  pass
 # channel = forms.CharField(
 #   label=_("Channel"),
 #   strip=False,
 #   widget=forms.TextInput,
 # )
