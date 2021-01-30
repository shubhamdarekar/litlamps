from django.urls import path, include

from ecom import views

urlpatterns = [
    path('', views.homepage),
    path('temp/', views.template),
    path('product/', views.product_page),
    path('products/', views.products),
    path('accounts/', include('allauth.urls')),
    path('checkout/', views.checkout),
    path('logout/', views.logout_view),
    path('add_to_cart/', views.add_to_cart),
    path('remove_from_cart/', views.remove_from_cart),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
]
