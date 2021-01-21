# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.BooleanField()
    email_id = models.CharField(max_length=255)
    mobile_no = PhoneNumberField(null=False, blank=False, unique=True)

class Password(models.Model):
    customer_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    product_quantity = models.IntegerField()
    product_price_rupees = models.FloatField()
    product_price_dollars = models.FloatField()
    bestselling = models.IntegerField()
    image_path = models.TextField()

class Orders(models.Model):
    customer_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.TextField()
    amount = models.BigIntegerField()
    order_success = models.BooleanField()
    payment = models.BooleanField()

class Order_items(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

class Customer_reviews(models.Model):
    customer_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField()

class FAQs(models.Model):
    question = models.TextField()
    answer = models.TextField()

class Ratings(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()

class Recently_viewed(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)