import razorpay
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.db import connection
from django.contrib.auth.models import User as authUser

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
        if request.user.is_authenticated:
            temp = Recently_viewed()
            temp.product_id = id
            temp.customer_id = request.user.id
            temp.save()
    return render(request, 'product_page.html', {'id': id, 'product_details': product_details, 'cart': cart})


def checkout(request):
    cart = cart_items(request)
    totalPrice = Cart.objects.filter(customer_id=request.user.id).aggregate(Sum('product__product_price_rupees'))
    return render(request, 'checkout.html', {'cart': cart, 'totalPrice': totalPrice['product__product_price_rupees__sum']})


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

def profile(request):
    if request.user.is_authenticated:
        address = Address.objects.filter(customer_id=request.user.id)
        return render(request, 'profile.html', {'addresses': address})
    else:
        return redirect('/accounts/google/login')

def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            user = authUser.objects.get(email=request.POST['email'])
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            return redirect('/profile/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def create_razorpay_order(request):
    if request.method == 'GET' and request.GET['type'] == 'cart':
        # Find total price
        total_price = Cart.objects.filter(customer_id=request.user.id).aggregate(Sum('product__product_price_rupees'))
        order_amount = total_price['product__product_price_rupees__sum']

        # Make razorpay order
        order_currency = 'INR'
        notes = {'Shipping address': 'test', 'amount': order_amount}
        temp_client = razorpay.Client(auth=("rzp_test_XgSvcOhAnzdFER", "4gwNXfK8dXaeAkkKAKGIByhT"))
        data = {'amount': order_amount * 100, 'currency': order_currency, 'notes': notes,
                'payment_capture': '1'}
        payment = temp_client.order.create(data=data)
        print(payment)

        # create new order
        new_order = Order()
        new_order.amount = order_amount
        new_order.customer_id = request.user.id
        new_order.razorpay_order_id = payment['id']
        new_order.save()

        # fill all the items in order
        cart_all = cart_items(request)
        for item in cart_all:
            new_order_item = Order_item()
            new_order_item.order_id = new_order.id
            new_order_item.quantity = item.quantity
            new_order_item.product_id = item.product_id
            new_order_item.save()

    return render(request, 'payment_completion.html', {'payment': payment})


def success_redirect(request):
    razorpay_payment_id = request.POST['razorpay_payment_id']
    razorpay_order_id = request.POST['razorpay_order_id']
    razorpay_signature = request.POST['razorpay_signature']
    temp_client = razorpay.Client(auth=("rzp_test_XgSvcOhAnzdFER", "4gwNXfK8dXaeAkkKAKGIByhT"))
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    temp_client.utility.verify_payment_signature(params_dict)
    order_obj = Order.objects.get(razorpay_order_id=razorpay_order_id)
    order_obj.payment = True
    order_obj.payment_id = razorpay_payment_id
    order_obj.save()
    Cart.objects.filter(customer_id=request.user.id).delete()
    return render(request, 'payment_success.html', {'data': request.POST})


def orders_page(request):
    return render(request, "orders_page.html")

def add_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            temp = request.POST['address']
            address = Address()
            address.address = temp
            address.customer_id = request.user.id
            address.save()
    return redirect('/profile')

def delete_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST['id']
            Address.objects.filter(id=id).delete()
    return redirect('/profile')
