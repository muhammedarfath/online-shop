from django.contrib import admin
from .models import Order, OrderProduct, Payment, ShopCart

    
    
    
admin.site.register(ShopCart)    
admin.site.register(Order)    
admin.site.register(OrderProduct)
admin.site.register(Payment)    
