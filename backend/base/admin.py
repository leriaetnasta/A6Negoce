from django.contrib import admin
from .models import *
from shop.models import *

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(AdminUser)
admin.site.register(User)
admin.site.register(Costumer)