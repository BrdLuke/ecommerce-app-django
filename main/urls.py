from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about-us/', views.about_us_view, name="about_us"),
    path('find-us/', views.find_us_view, name="find_us"),
    path('contact-us/', views.contact_us_view, name="contact_us"),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('userDetails/<int:pk>/profile', views.details_user, name = 'user_details'),
    path('updateDetails/', views.update_user_details, name = 'update_user'),
    path('products/', views.products_list, name = 'products'),
    path('product/<str:product_name>/', views.details_product, name = 'product_details'),
    path('cart/checkout/product/<str:product_name>', views.checkout, name = 'checkout'),
    path('cart/<int:pk>', views.add_to_cart, name = 'add_to_cart'),
    path('cart/delete_<int:pk>', views.delete_from_cart, name = 'delete_from_cart'),
    path('cart/checkout/<int:pk>', views.checkout_cart, name = "checkout_cart")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'main.views.custom_404'