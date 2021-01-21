from django.contrib import admin

# Register your models here.
from ecom.models import *

admin.site.register(Users)
admin.site.register(Password)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Order_items)
admin.site.register(Customer_reviews)
admin.site.register(FAQs)
admin.site.register(Ratings)
admin.site.register(Recently_viewed)


