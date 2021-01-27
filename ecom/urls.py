from django.urls import path, include

from ecom import views

urlpatterns = [
    path('', views.homepage),
    path('temp/', views.template),
    path('product/', views.product_page),
    path('products/', views.products),
    path('accounts/', include('allauth.urls')),
]
