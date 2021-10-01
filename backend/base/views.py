from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
from shop.models import *
from shop.forms import *
from django.http import HttpResponse
import csv
from .utils import get_plot
import pandas as pd
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group

def has_group(user, group):
    return user.groups.filter(name=group).exists()



# Create your views here.
class ProductView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request):
        form=ProductForm()
        return render(request,"admins/product_form.html",{'form':form})
    def post(self,request):
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
           form.save()
        return redirect("base:productList")
        
class CategoryView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request):
        form=CategoryForm()
        return render(request,"admins/category_form.html",{'form':form})
    def post(self,request):
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
           form.save()
        return redirect("base:categoryList")

class ProductUpdateView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        product=Product.objects.get(id=idp)
        form=ProductForm(instance=product)
        return render(request,"admins/product_form.html",{'form':form})
    def post(self,request,idp):
        product=Product.objects.get(id=idp)
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
           form.save()
        return redirect("base:productList")

class CategoryUpdateView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        category=Category.objects.get(id=idp)
        form=CategoryForm(instance=category)
        return render(request,"admins/category_form.html",{'form':form})
    def post(self,request,idp):
        category=Category.objects.get(id=idp)
        form=CategoryForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
           form.save()
        return redirect("base:categoryList")

class ProductDeleteView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        return render(request,"admins/delete_form.html",{})
    def post(self,request,idp):
        product=Product.objects.get(id=idp)
        product.delete()
        return redirect("base:productList")

class CategoryDeleteView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        return render(request,"admins/catdelete_form.html",{})
    def post(self,request,idp):
        category=Category.objects.get(id=idp)
        category.delete()
        return redirect("base:categoryList")

class ProductDetailsView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        product=Product.objects.get(id=idp)
        return render(request,"admins/product_details.html",{'product':product})

class CategoryDetailsView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request,idp):
        category=Category.objects.get(id=idp)
        return render(request,"admins/category_details.html",{'category':category})


class IndexView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self, request):
        return render(request,"admins/base.html",{})

class ProductListView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request):
        products=Product.objects.all()
        return render(request,"admins/product_list.html",{'products':products})

class CategoryListView(UserPassesTestMixin,View):
    def test_func(self):
        qs=self.request.user
        return has_group(qs,'admins')
    def get(self,request):
        categories=Category.objects.all()
        return render(request,"admins/category_list.html",{'categories':categories})


def export(request):
    response= HttpResponse(content_type='text/csv')
    writer=csv.writer(response,delimiter=',')
    writer.writerow(['name','description','brand','price','countInStock','category'])
    for task in Product.objects.all().values_list('name','description','brand','price','countInStock','category'):
        writer.writerow(task)
    response['Content-Disposition']= 'attachement ; filename="Product.csv"'
    return response


def graph_view(request):
    qs=OrderItem.objects.all()
    x=[x.product.name for x in qs]
    y=[y.quantity for y in qs]
    chart=get_plot(x,y)
    return render(request,"admins/graph.html",{'chart':chart})



class AddAdminUserView(View):
    def get(self,request):
        user_form = UserForm()
        admin_form = AdminUserForm(request.POST)
        return render(request,'admins/admin_form.html',{'user_form': user_form,'admin_form':admin_form})
    def post(self,request):
        user_form = UserForm(request.POST)
        admin_form = AdminUserForm(request.POST,request.FILES)

        if user_form.is_valid() and admin_form.is_valid():
            new_user = user_form.save(commit=False)
            # Définir le mot de passe choisi
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_admin=True
            
            new_user.save()
            group = Group.objects.get(name='admins')
            new_user.groups.add(group)
            new_admin=admin_form.save(commit=False)
            new_admin.user=new_user
            new_admin.save()
            return render(request,'admins/admin_users_list.html',{'new_user': new_user})
        return HttpResponse('Données invalides')

def AdminUserListView(request):
        adminUsers=AdminUser.objects.all()
        return render(request,"admins/admin_users_list.html",{'adminUsers':adminUsers})

def CostumerUserListView(request):
        costumers=Costumer.objects.all()
        return render(request,"admins/Costumer_users_list.html",{'costumers':costumers})


class User_login(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'admins/login.html', {'form': form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active and user.is_admin:
                    login(request, user)
                    return redirect("base:productList")
                else:
                    return HttpResponse("you're not an admin")
            else:
                return HttpResponse('Invalid login')
        return redirect("base:home")

def user_logout(request):
    logout(request)
    return redirect("shop:shop")


def order_history(request):
    orders = Order.objects.all()
    return render(request, "admins/commandes_list.html", {'orders':orders})