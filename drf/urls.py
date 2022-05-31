from .import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'brand', views.BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    # path('brandx/', views.getBrandData),
    # path('brandx/add/', views.addBrand),
]
