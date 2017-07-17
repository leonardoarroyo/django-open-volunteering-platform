from ovp_faq.models.category import Category

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.compat import set_many
from rest_framework.utils import model_meta

class CategoryFaqRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name']
