import razorpay
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from razorpay import client
from django.contrib.auth import logout

from .models import *


# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('/')


def recent_viewed():
    recently = Recently_viewed.objects.all()
    return recently


def template(request):
    return render(request, 'template.html')


def product_page(request):
    id = 0
    if request.method == 'GET':
        id = request.GET['id']
        product_details = Product.objects.get(id=id)
    return render(request, 'product.html', {id: id, 'product_details': product_details})


def checkout(request):
    cart = cart_items(request)
    return render(request, 'checkout.html', {'cart': cart})


def homepage(request):
    payment = ''
    if request.method == 'POST':
        order_amount = 50000
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': 'Bommanahalli, Bangalore'}
        temp_client = razorpay.Client(auth=("rzp_test_XgSvcOhAnzdFER", "4gwNXfK8dXaeAkkKAKGIByhT"))
        data = {'amount': order_amount, 'currency': order_currency, 'receipt': order_receipt, 'notes': notes,
                'payment_capture': '1'}
        # payment = temp_client.order.create(data=data)

    bestselling = Product.objects.all().order_by('bestselling')
    faq = FAQ.objects.all()
    recently_viewed = recent_viewed()
    cart = cart_items(request)
    return render(request, 'index2.html',
                  {'bestselling': bestselling, 'faq': faq, 'payment': payment, 'cart': cart})


def login(request):
    pass


def cart_items(request):
    uid = request.user.id
    cart = Cart.objects.filter(customer_id=uid)
    return cart


def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products});
