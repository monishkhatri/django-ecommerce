from rest_framework import serializers
from coreapp.models import Brand, Category, Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(read_only=True)
    subcategory = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Product
        fields = ['category', 'subcategory', 'brand', 'user', 'title', 'desc_short', 'actual_price', 'stock_count', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    parent = serializers.CharField(read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'parent', 'status', 'created_at']

    def get_status(self,obj):
        return obj.get_status_display()

class CategoryClassBasedSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Category
        fields = ['name', 'parent', 'status', 'created_at']

class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)    
    status = serializers.SerializerMethodField()
    description = serializers.CharField()

    def get_status(self,obj):
        return obj.get_status_display()

    def create(self, validated_data):
        return Brand.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('status', instance.description)
        instance.save()
        return instance

class BrandFuncSerializer(serializers.ModelSerializer):
    """
        Diffrence B/w Model & HyperLinkModel
        - It does not include the id field by default.
        - It includes a url field, using HyperlinkedIdentityField.
        - Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
    """
    class Meta:
        model = Brand
        fields = ['name', 'description']
        # fields = '__all__'
