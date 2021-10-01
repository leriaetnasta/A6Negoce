from django import forms
from base.models import Order
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
class UserForm(forms.ModelForm):
    password = forms.CharField(label='Le mot de passe"',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Répéter le mot de passe',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email')
        labels={"first_name":"Prénom",
                "last_name":"Nom",
                "username":"Nom d'utilisateur",
                "email":"Email"}
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
   
class CostumerForm(forms.ModelForm):
    class Meta:
        model = Costumer
        fields = ('date_of_birth', 'photo')
        labels={"date_of_birth":"Date de naissance"}
    
class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput,label="le mot de passe")
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 50)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    class Meta:
        labels={"quantity":"Quantité"}
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','postal_code', 'city']
        labels={"address":"Adresse",
                "postal_code":"Code postal",
                "city":"Ville"}
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        