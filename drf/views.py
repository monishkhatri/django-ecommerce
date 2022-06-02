from unicodedata import category
from rest_framework import viewsets
from rest_framework import permissions
from coreapp.models import Brand, Category, Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf import serializers as serializeCls
# For Class based view
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status

class CategoryClassBased(APIView):
    def get(self, request, format=None):
        snippets = Category.objects.all()
        serializer = serializeCls.CategoryClassBasedSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializeCls.CategoryClassBasedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryClassBasedList(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializeCls.CategoryClassBasedSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializeCls.CategoryClassBasedSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductSerializer(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_published=1).order_by('-created_at')
    serializer_class = serializeCls.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            category=Category.objects.get(id=1),
            subcategory=Category.objects.get(id=2),
            brand=Brand.objects.get(id=1)
        )
    
class CategorySerializer(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status=1).order_by('-created_at')
    serializer_class = serializeCls.CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.filter(status=1).order_by('-created_at')
    serializer_class = serializeCls.BrandSerializer
    # permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST'])
def getBrandData(request):
    if request.method == "GET":
        items = Brand.objects.filter(status=1)
        serializer = serializeCls.BrandFuncSerializer(items, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializers = serializeCls.BrandFuncSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)
