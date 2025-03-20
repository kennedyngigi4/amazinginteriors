from django.urls import path
from apps.website.views import *

urlpatterns = [
    path( "", IndexView, name="index", ),
    path( "about_us", AboutView, name="about_us", ),
    path( "shop", ShopView, name="shop", ),
    path( "product_details/<str:pk>/<str:name>", ProductDetailsView, name="product_details", ),
    path( "services", ServicesView, name="services", ),
    path( "contact", ContactsView, name="contact", ),
    path( "favorites", FavoritesView, name="favorites", ),

    path( "sign_up", SignUpView, name="sign_up", ),
    path( "sign_in", SignInView, name="sign_in", ),

    path( "add_to_cart", addToCart, name="add_to_cart", ),
    path( "cart", CartView, name="cart", ),
    path( "checkout", CheckOutView, name="checkout", ),
    path( "sub_counties", SubCountiesView, name="sub_counties"),
]


# Logged in user links
urlpatterns += [
    path( "user_dashboard", UserDashboard, name="user_dashboard", ),
    path( "user_orders", UserOrders, name="user_orders", ),
    path( "user_address", UserAddress, name="user_address", ),
    path( "user_password_manager", UserPasswordManager, name="user_password_manager", ),
    path( "logout", UserLogOut, name="logout", ),
]



