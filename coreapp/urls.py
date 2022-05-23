from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),

    ### AUTHENTICATION
    path('login/', views.handleSignin, name='BlogLogin'),
    path('register/', views.handleSignup, name='BlogRegister'),
    path('logout/', views.handleLogout, name='BlogLogout'),
    ### PRODUCT RELATED
    path('<slug:slug>/', views.productDetail.as_view(), name='productDetail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
