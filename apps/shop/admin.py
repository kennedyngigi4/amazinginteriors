from django.contrib import admin
from apps.shop.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Payment)
