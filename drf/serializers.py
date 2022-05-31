from rest_framework import serializers
from coreapp.models import Brand

class BrandxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'description']
        # fields = '__all__'
