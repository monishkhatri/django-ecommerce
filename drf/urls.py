from .import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'brand', views.BrandViewSet)
router.register(r'category', views.CategorySerializer)
router.register(r'product', views.ProductSerializer)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('brand-function-based-view/', views.getBrandData),
    path('category-class-based-view/', views.CategoryClassBased.as_view()),
    path('category-class-based-view/<int:pk>/', views.CategoryClassBasedList.as_view()),
]