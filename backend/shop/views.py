from django.shortcuts import render,redirect
from django.views import View
from base.models import *
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def has_group(user, group):
    return user.groups.filter(name=group).exists()

def rechercher(request):
    products=Product.objects.filter(name__icontains=request.POST.get("cle"))
    return render(request,"clients/product_list.html",{'products':products})

class IndexView(View):
    def get(self,request):
        products=Product.objects.all()
        cart_product_form = CartAddProductForm()
        contactform=ContactForm()
        return render(request,"clients/index.html",{'products':products,'cart_product_form':cart_product_form,'contactform':contactform})
    def post(self,request):
        contactform=ContactForm(request.POST,request.FILES)
        if contactform.is_valid():
           contactform.save()
           email_subject = f'New contact {contactform.cleaned_data["email"]}: {contactform.cleaned_data["subject"]}'
           email_message = contactform.cleaned_data['message']
           send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
        else:
            return HttpResponse('Données invalides')
        return redirect("shop:shop")



class ProductListView(View):
    def get(self,request):
        products=Product.objects.all()
        cart_product_form = CartAddProductForm()
        return render(request,"clients/product_list.html",{'products':products,'cart_product_form':cart_product_form})
        
class ProductsByCategoryView(View):
    def get(self,request,idc):
        products=Product.objects.filter(category_id=idc)
        return render(request,"clients/product_list.html",{'products':products})

class Register(View):
    def get(self,request):
        user_form = UserForm()
        costumer_form = CostumerForm()
        return render(request,'clients/register.html',{'user_form': user_form,'costumer_form':costumer_form})
    def post(self,request):
        user_form = UserForm(request.POST)
        costumer_form = CostumerForm(request.POST,request.FILES)

        if user_form.is_valid() and costumer_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_costumer=True
            
            new_user.save()
            group = Group.objects.get(name='costumers')
            new_user.groups.add(group) 
            new_costumer=costumer_form.save(commit=False)
            new_costumer.user=new_user
            new_costumer.save()
            return render(request,'clients/shop.html',{'new_user': new_user})
        return HttpResponse('Données invalides')

class User_login(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'clients/login.html', {'form': form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_admin:
                        return redirect('base:home')
                    else :
                        return redirect('shop:shop')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Données invalides')
        return redirect("shop:shop")

def user_logout(request):
    logout(request)
    return redirect('shop:shop')

def cart_add(request, product_id):
    cart = request.session.get(settings.CART_SESSION_ID,{})
    product = Product.objects.get(id=product_id)
    product_id = str(product.id)
    if product_id not in cart:
            cart[product_id] = {'quantity': 1,'price': product.price}

    request.session[settings.CART_SESSION_ID]=cart

    return redirect('shop:productList')

def cart_detail(request):
    cart = request.session.get(settings.CART_SESSION_ID,{})
    cart_total_price=0

    for key,val in cart.items():
        product = Product.objects.get(id=key)
        cart[str(product.id)]['product']=product
        cart[str(product.id)]['price'] = product.price
        cart[str(product.id)]['total_price'] = float(cart[str(product.id)]['price']) * float(cart[str(product.id)]['quantity'])
        cart_total_price+=cart[str(product.id)]['total_price']
    
    return render(request, 'clients/shopcart.html', {'cart': cart,'cart_total_price':cart_total_price})

def cart_update(request, product_id):
    cart = request.session.get(settings.CART_SESSION_ID)
    product = Product.objects.get(id=product_id)
    cart[str(product_id)]['quantity']=request.POST.get('quantity')
    request.session[settings.CART_SESSION_ID]=cart

    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart=request.session.get(settings.CART_SESSION_ID)
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session[settings.CART_SESSION_ID]=cart
    return redirect('shop:cart_detail')
def is_costumer(user):
    if user.is_authenticated and user.is_costumer:
        return True
    return False

@user_passes_test(is_costumer, login_url='/login/')
def order_create(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.paid=True
            order.costumer=request.user.costumer
            order.save()

            for key,val in cart.items():
                product = Product.objects.get(id=int(key))
                OrderItem.objects.create(order=order,product=product,price=val['price'],quantity=val['quantity'])
            # Vider le panier
            del request.session[settings.CART_SESSION_ID]
            return render(request,'clients/payed.html', {'order': order})
    else:
        cart_total_price=0
        for key,val in cart.items():
            cart_total_price+= float(cart[key]['price']) * float(cart[key]['quantity'])
        form = OrderCreateForm()
        return render(request,'clients/processing_cmd.html',{'form': form,'cart_total_price':cart_total_price})


def order_history(request, user_id):
    orders = Order.objects.filter(costumer_id=user_id)

    return render(request, "clients/mescommandes.html", {'orders':orders})