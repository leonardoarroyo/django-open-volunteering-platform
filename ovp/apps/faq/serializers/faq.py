from ovp.apps.faq.models.faq import Faq
from ovp.apps.faq.serializers.category import CategoryFaqRetrieveSerializer

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.compat import set_many
from rest_framework.utils import model_meta

class Faq(serializers.ModelSerializer):
	category = CategoryFaqRetrieveSerializer()
	class Meta:
		model = Faq
		fields = ['id', 'question', 'answer', 'category']
