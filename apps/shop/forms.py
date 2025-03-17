from django import forms
from apps.shop.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name"
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "price", "size", "colors", "material", "category", "main_image", "in_stock", "description", "additional_info"
        ]

