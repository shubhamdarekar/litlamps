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
    path('removeFromCartajax/', views.remove_from_cart_ajax),
    path('createRzpOrder/', views.create_razorpay_order),
    path('successRedirect/', views.success_redirect),
    path('orders/', views.orders_page),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
    path('add_address/', views.add_address),
    path('delete_address/', views.delete_address),
    path('buy_now/', views.checkout_product),
    path('submitReview/', views.write_review),
    path('privacy/', views.privacy_policy),
    path('termsconditions/', views.term_condition),
    path('refundPolicy/', views.refund_policy),
    path('accounts/google/login/callback/<str:path>/', views.redirection),


]
