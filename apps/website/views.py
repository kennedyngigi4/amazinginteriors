from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.shop.models import *

from apps.accounts.forms import *
# Create your views here.



def IndexView(request):
    context = {}
    return render(request, "website/index.html", context)



def AboutView(request):
    context = {}
    return render(request, "website/about_us.html", context)


def ShopView(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by("name")
    context = {
        "products": products,
        "categories": categories
    }
    return render(request, "website/shop.html", context)


def ProductDetailsView(request, pk=None, name=None):
    product = Product.objects.get(product_id=pk)
    context = {
        "product": product
    }
    return render(request, "website/product_details.html", context)


def ServicesView(request):
    context = {}
    return render(request, "website/services.html", context)


def ContactsView(request):
    context = {}
    return render(request, "website/contact_us.html", context)



def SignUpView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                fullname=request.POST.get("fullname"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
            )
            user.save()
            return JsonResponse({ "success": True, "message": "Account created" })
        else:
            return JsonResponse({ "success": False, "message": "Sorry something went wrong." })

    context = {}
    return render(request, "website/sign_up.html", context)



def SignInView(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_admin:
                    return JsonResponse({ "success":True, "message": "Login successful", "url": "manager/dashboard" })
                else:
                    return JsonResponse({ "success":True, "message": "Login successful", "url": "/user_dashboard" })
                
            else:
                return JsonResponse({ "success":False, "message": "Invalid email or password"})
        else:
            return JsonResponse({ "success":False, "message": "Invalid email or password"})
    context = {}
    return render(request, "website/sign_in.html", context)


def addToCart(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, product_id=product_id)

    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart

    return JsonResponse({ "message": "Product added to cart", "cart_count": len(cart) })



def CartView(request):
    cart_items = []
    cart = request.session.get("cart", {})
    total_price = 0
    total_items = 0
    
    for product_id, quantity in cart.items():
        product = Product.objects.get(product_id=product_id)
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "total_price": product.price * quantity,
        })

        total_items += quantity
        total_price += product.price * quantity

    return render(request, "website/cart.html", { "cart_items": cart_items, "total_items": total_items, "total_price": total_price })


def SubCountiesView(request):
    selected_county = request.GET.get("county")
    county = County.objects.get(name=selected_county)
    subcounties = SubCounty.objects.filter(county=county.id).order_by("name").values("name","county","id")
    return JsonResponse(list(subcounties), safe=False)


@login_required(login_url="sign_in")
def CheckOutView(request):
    counties = County.objects.all().order_by("name")
    cart_items = []
    session_cart = request.session.get("cart", {})
    total_price = 0
    total_items = 0
    
    for product_id, quantity in session_cart.items():
        product = Product.objects.get(product_id=product_id)
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "total_price": product.price * quantity,
        })

        total_items += quantity
        total_price += product.price * quantity

    if request.method == "POST":
        phone = request.POST.get("phone")
        location=request.POST.get("location")
        if session_cart:
            cart = Cart.objects.create(user=request.user, total_price=total_price,total_items=total_items,phone=phone,location=location)
            for product_id, quantity in session_cart.items():
                product = Product.objects.get(product_id=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, price_at_purchase=product.price)
                if not created:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = quantity
                cart_item.save()
        request.session["cart"] = {}
        return JsonResponse({ "success": True, "message": "Order successful!" })

    context = {
        "counties": counties,
        "cart_items": cart_items,
        "total_items": total_items,
        "total_price": total_price
    }
    return render(request, "website/checkout.html", context)



@login_required(login_url="sign_in")
def UserDashboard(request):
    context = {}
    return render(request, "website/user/dashboard.html", context)



@login_required(login_url="sign_in")
def UserOrders(request):
    orders = Cart.objects.filter(user=request.user).prefetch_related("items__product").order_by("-created_at")
    context = {
        "orders": orders
    }
    return render(request, "website/user/my_orders.html", context)



@login_required(login_url="sign_in")
def UserAddress(request):
    context = {}
    return render(request, "website/user/manage_address.html", context)




@login_required(login_url="sign_in")
def UserPasswordManager(request):
    context = {}
    return render(request, "website/user/password_manager.html", context)


# @login_required(login_url="sign_in")
def UserLogOut(request):
    logout(request)
    return redirect("/sign_in")

