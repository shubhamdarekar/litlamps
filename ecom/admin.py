from django.contrib import admin

# Register your models here.
from ecom.models import *

admin.site.register(User)
admin.site.register(Password)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Customer_review)
admin.site.register(FAQ)
admin.site.register(Rating)
admin.site.register(Recently_viewed)
admin.site.register(Cart)


