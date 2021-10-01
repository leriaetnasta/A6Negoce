from base.models import Category
from django.conf import settings

def cart(request):
   return {'cart': request.session.get(settings.CART_SESSION_ID)}

def categories(request):
   categories=Category.objects.all()
   return {'categories': categories}