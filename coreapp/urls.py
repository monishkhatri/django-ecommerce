from . import views
from coreapp import cart
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
    path('contact/', views.contactView, name='contact'),

    #CART RELATED 
    path('my-cart/', views.cartDetail, name='mycart'),
    path('my-cart/add/<int:id>/', views.cartAdd, name='cart_add'),
    path('my-cart/remove/<int:id>/', views.cartDeleteProduct, name='cart_add'),
    path('my-cart/clearitem/<int:id>/', views.cartItemclear, name='cart_clear'),
    path('my-cart/clear', views.cartClear, name='cart_clear'),

    ### NOTE :: This should be written in last else it will face many errors
    ### PRODUCT RELATED ROUTES
    path('checkout/', views.checkoutView, name='checkout'),
    path('category/<slug:slug>/', views.categoryView, name='categoryView'),
    path('<slug:slug>/', views.productDetail.as_view(), name='productDetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
