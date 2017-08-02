from rest_framework import serializers
from ovp.apps.projects import models

class CategoryRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Category
		fields = ['id', 'name', 'description', 'image', 'highlighted', 'slug']