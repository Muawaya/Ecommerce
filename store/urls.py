from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("category/<str:foo>/", views.category, name="category"),
    path("cart/summary/", views.cart_summary, name="cart_summary"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/delete/", views.cart_delete, name="cart_delete"),
    path("cart/update/", views.cart_update, name="cart_update"),
    
]
