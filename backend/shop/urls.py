from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.IndexView.as_view(),name="shop"),
    path('products/', views.ProductListView.as_view(),name="productList"),
    path('caregories/<int:idc>/products/', views.ProductsByCategoryView.as_view(),name="productByCetgorie"),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.User_login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_detail,name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.cart_remove,name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('create/', views.order_create, name='order_create'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('mescommandes/<int:user_id>/', views.order_history, name='history'),



]


