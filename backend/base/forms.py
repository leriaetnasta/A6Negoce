from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels={"name":"Nom",
                "description":"Description",
                "brand":"Marque",
                "price":"Prix",
                "countInStock":"Quantité en stock",
                "category":"Catégorie"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        labels={"name":"Nom",
                "description":"Description"}

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ('date_of_birth', 'photo')
        labels={"date_of_birth":"Date de naissance"}