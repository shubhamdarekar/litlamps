# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.BooleanField()
    email_id = models.CharField(max_length=255)
    mobile_no = PhoneNumberField(null=False, blank=False, unique=True)

class Password(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    product_quantity = models.IntegerField()
    product_price_rupees = models.FloatField()
    product_price_dollars = models.FloatField()
    bestselling = models.IntegerField(null=True)
    image_path = models.TextField()

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    amount = models.BigIntegerField()
    order_success = models.BooleanField()
    payment = models.BooleanField()

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

class Customer_review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()

class Recently_viewed(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)