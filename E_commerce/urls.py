"""
URL configuration for E_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shopswift import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('logout',views.logout, name = 'logout'),
    path('create/', views.createAccount),
    path('login/',views.login),
    path('home/',views.home),
    path('addproduct/',views.AddProduct),
    path('buy/<int:id>/',views.ViewProduct),
    path('favorite',views.AddToCart, name='favorite'),
    path('search',views.search_view),
    path('price_filiter',views.price_filitering),
    # path('sea',views.prp),
    path('verify_otp/',views.otp_validation, name='verify_otp'),
    path('send_otp/',views.forgot_password, name='send_otp'),
    path('delete/<int:id>/',views.cart_product_remove),
    path('product/<str:id>/',views.product_category),
    path('orders',views.order_product),
    path('remove/<int:id>/',views.order_product_remove),
    # path('AdminDashboard',views.admin),
    # path('sellers',views.sellers),
    path('orderconfirm',views.order_successfull),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

