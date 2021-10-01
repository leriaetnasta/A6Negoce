from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('graph',views.graph_view,name='graph'),
    path('export-csv',views.export,name='exportcsv'),
    path('login/', views.User_login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('adminUsers/create', views.AddAdminUserView.as_view(),name="adminUsersCreate"),
    path('adminUsers/', views.AdminUserListView,name="adminUsersList"),
    path('costumerUsers/', views.CostumerUserListView,name="costumerUsersList"),
    path('products/create',views.ProductView.as_view(),name='productCreate'),
    path('products/',views.ProductListView.as_view(),name='productList'),
    path('products/<int:idp>/update',views.ProductUpdateView.as_view(),name='productUpdate'),
    path('products/<int:idp>/delete',views.ProductDeleteView.as_view(),name='productDelete'),
    path('products/<int:idp>/details',views.ProductDetailsView.as_view(),name='productDetails'),
    path('categories/create',views.CategoryView.as_view(),name='categoryCreate'),
    path('categories/',views.CategoryListView.as_view(),name='categoryList'),
    path('categories/<int:idp>/delete',views.CategoryDeleteView.as_view(),name='categoryDelete'),
    path('categories/<int:idp>/details',views.CategoryDetailsView.as_view(),name='categoryDetails'),
    path('categories/<int:idp>/update',views.CategoryUpdateView.as_view(),name='categoryUpdate'),
    path('Commandes/', views.order_history, name='history'),


   ]