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
    ### STATIC PAGE 
    path('contact/', views.contactView, name='mycart'),
    ### PRODUCT RELATED
    path('my-cart/', views.cartView, name='mycart'),
    path('checkout/', views.checkoutView, name='checkout'),
    path('category/<slug:slug>/', views.categoryView, name='categoryView'),
    path('<slug:slug>/', views.productDetail.as_view(), name='productDetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
