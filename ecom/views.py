from django.shortcuts import render
from .models import *


# Create your views here.
def recent_viewed():
    recently = Recently_viewed.objects.all()
    return recently


def homepage(request):
    bestselling = Product.objects.all().order_by('bestselling')
    products = Product.objects.all()
    faq = FAQ.objects.all()
    recently_viewed = recent_viewed()
    return render(request, 'index.html', {'bestselling': bestselling, 'products': products, 'faq': faq})

def login(request):
    pass

def cart_items():
    cart = Cart.objects.all()
    return cart


