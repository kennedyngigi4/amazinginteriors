from django.urls import path
from apps.manager.views import *


app_name = "manager"

urlpatterns = [
    path( "orders-data", OrderStatsView, name="orders-data", ),
    path( "dashboard/", ManagerDashboard, name="dashboard", ),
    path( "categories/", ManagerCategories, name="categories", ),
    path( "create_product/", ManagerCreateProduct, name="create_product", ),
    path( "products/", ManagerProducts, name="products", ),
    path( "product_details/<str:pk>", ManagerProduct, name="product_details", ),
    path( "product_delete/<str:pk>", ManagerDeleteProduct, name="product_delete", ),
    path( "orders/", ManagerOrders, name="orders", ),
    path( "order_details/<str:pk>", ManagerOrderDetails, name="order_details", ),
    path( "payments/", ManagerPayments, name="payments", ),
    path( "users/", ManagerUsers, name="users", ),
]

