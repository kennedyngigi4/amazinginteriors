import json
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Count, Sum
from apps.shop.forms import CategoryForm, ProductForm
from apps.shop.models import *
from datetime import timedelta

# Create your views here.

@staff_member_required(login_url="sign_in")
def OrderStatsView(request):
    total_orders = Cart.objects.all().count()
    total_users = User.objects.all().exclude(uid=request.user.uid).count()
    total_payments = Payment.objects.aggregate(total_amount=Sum("amount"))["total_amount"] or 0

    today = timezone.now().date()
    last_14_days = [today - timedelta(days=i)  for i in range(13, -1, -1)]

    orders_count = ( 
        Cart.objects.filter(created_at__date__gte=today - timedelta(days=13))
        .values("created_at__date")    
        .annotate(order_count=Count("cart_id"))
    )

    payments_count = (
        Payment.objects.filter(created_at__date__gte=today-timedelta(days=13))
        .values("created_at__date")
        .annotate(payment_count=Count("payment_id"))
    )   

    orders_dict = {str(order["created_at__date"]): order["order_count"]  for order in orders_count}
    payments_dict ={str(payment["created_at__date"]): payment["payment_count"] for payment in payments_count}

    data = {
        "labels": [day.strftime("%Y-%m-%d") for day in last_14_days],
        "data": [ orders_dict.get(str(day), 0) for day in last_14_days ],
        "payments": [payments_dict.get(str(day), 0) for day in last_14_days],
        "total_orders": total_orders,
        "total_users": total_users,
        "total_payments": total_payments
    }

    return JsonResponse(data)


@staff_member_required(login_url="sign_in")
def ManagerDashboard(request):
    context = {}
    return render(request, "manager/dashboard.html", context)


@staff_member_required(login_url="sign_in")
def ManagerCategories(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({ "success": True, "message": "Form submitted successfully"  })
        else:
            return JsonResponse({ "success": False, "message": form.errors  })

    context = {
        "categories": categories
    }
    return render(request, "manager/categories.html", context)


@staff_member_required(login_url="sign_in")
def ManagerCreateProduct(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return JsonResponse({ "success": True, "message": "Product added successfully" })
        else:
            return JsonResponse({ "success": False, "message": "Something went wrong" })
    context = {
        "categories": categories
    }
    return render(request, "manager/create_product.html", context)


@staff_member_required(login_url="sign_in")
def ManagerProducts(request):
    products = Product.objects.all().order_by("-created_at")
    context = {
        "products": products
    }
    return render(request, "manager/products.html", context)


@staff_member_required(login_url="sign_in")
def ManagerProduct(request, pk=None):
    product = get_object_or_404(Product, product_id=pk)
    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if not request.FILES.get('main_image'):
                form.instance.main_image = product.main_image

            if 'category' not in request.POST or request.POST.get("category") == "":
                form.instance.category = product.category

            if 'in_stock' not in request.POST or request.POST.get("in_stock") == "":
                form.instance.in_stock = product.in_stock

            form.save()
            return JsonResponse({ "success": True, "message": "Product updated!" })
        else:
            return JsonResponse({ "success": False, "message": form.errors })

    categories = Category.objects.all()
    
    context = {
        "categories": categories,
        "product": product,
    }
    return render(request, "manager/product.html", context)


@staff_member_required(login_url="sign_in")
def ManagerDeleteProduct(request, pk=None):
    if request.method == "POST":
        print(pk)
        product = get_object_or_404(Product, product_id=pk)
        
        if product:
            product.delete()
            return JsonResponse({ "success": True, "message": "Product deleted successfully"})
        else:
            return JsonResponse({ "success": False, "message": "Product not found"})


@staff_member_required(login_url="sign_in")
def ManagerOrders(request):
    orders = Cart.objects.all().prefetch_related("items__product")
    context = {
        "orders": orders
    }
    return render(request, "manager/orders.html", context)


@staff_member_required(login_url="sign_in")
def ManagerOrderDetails(request, pk=None):
    order = get_object_or_404(Cart, cart_id=pk)
    order_items = order.items.all()
    context = {
        "order": order,
        "order_items": order_items
    }
    return render(request, "manager/order.html", context)


@staff_member_required(login_url="sign_in")
def ManagerPayments(request):
    context = {}
    return render(request, "manager/payments.html", context)


@staff_member_required(login_url="sign_in")
def ManagerUsers(request):
    users = User.objects.filter().order_by("-date_joined")
    context = {
        "users": users
    }
    return render(request, "manager/users.html", context)






