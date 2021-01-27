from django.urls import path

from ecom import views

urlpatterns = [
    path('', views.homepage),
    path('temp/', views.template),
    path('product/', views.product_page),
    path('checkout/', views.checkout),

]
