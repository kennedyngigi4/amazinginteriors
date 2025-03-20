import uuid
import random, string
from django.db import models
from apps.accounts.models import *

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
    
    
class Material(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    colors = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to="products", null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    promotion_category = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


def generateOrderId():
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        digits = ''.join(random.choices(string.digits, k=3))
        ai_orderid = f"AI-{letters}{digits}"

        if not Cart.objects.filter(orderid=ai_orderid).exists():
            return ai_orderid
        

class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    payments = models.CharField(max_length=100, null=True, default="PENDING", blank=True)
    delivery = models.CharField(max_length=100, null=True, default="Processing", blank=True)
    orderid = models.CharField(max_length=15, default=generateOrderId, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.orderid} - {self.user.fullname}"



class CartItem(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.IntegerField(default=1)


    def total_price(self):
        return self.quantity * self.product.price


    def __str__(self):
        return f"{self.cart.orderid} - {self.product.name}"



class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)
    amount = models.IntegerField(default=1)
    payment_type = models.CharField(max_length=100, default="MPESA", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.transaction_id


class County(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
    

class SubCounty(models.Model):
    name = models.CharField(max_length=255, null=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.name} -{self.county.name}"

