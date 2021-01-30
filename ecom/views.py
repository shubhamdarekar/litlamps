import razorpay
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from razorpay import client
from django.contrib.auth import logout
from django.db import connection

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
    if request.method == 'GET':
        id = request.GET['id']
        product_details = Product.objects.get(id=id)
        cart = cart_items(request)
        # print(product_detail)
    return render(request, 'product.html', {'id': id, 'product_details': product_details, 'cart': cart})


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
    cart_visible = 0
    if request.method == 'GET' and 'cart' in request.GET and request.GET['cart'] == 'true':
        cart_visible = 1
    products = Product.objects.all()
    cart = cart_items(request)
    return render(request, 'products.html', {'products': products, 'cart': cart, 'cart_visible': cart_visible});

def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['id']:
                cursor = connection.cursor()
                product_id = request.POST['id']
                customer_id = request.user.id
                cursor.execute('select * from ecom_cart where product_id = %s and customer_id = %s', [product_id, customer_id])
                row = list(cursor.fetchall())
                print(row)
                if row:
                    Cart.objects.filter(id=row[0][0]).update(quantity=row[0][3] + 1)
                else:
                    cart = Cart()
                    cart.product_id = request.POST['id']
                    cart.customer_id = request.user.id
                    cart.save()
                return redirect('/products/?cart=true')
    else:
        return redirect('/accounts/google/login')


def remove_from_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['id']:
                print('Hello')
                id = request.POST['id']
                next = request.POST.get('next', '/')
                # user = request.user.id
                obj = Cart.objects.filter(id=id).delete()
                print(obj)

                return HttpResponseRedirect(next + '?cart=true')
    else:
        return redirect('/')


