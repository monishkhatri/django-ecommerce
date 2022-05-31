from coreapp.models import Brand
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BrandSerializer, BrandxSerializer
# from drf import serializers

class BrandViewSet(viewsets.ModelViewSet):
    from rest_framework.authtoken.models import Token
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Brand.objects.filter(status=1).order_by('-created_at')
    serializer_class = BrandxSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def getBrandData(request):
    items = Brand.objects.filter(status=1)
    serializer = BrandSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addBrand(request):
    serializers = BrandSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)
