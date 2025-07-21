from django.contrib import admin
from .models import *
# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "created", "total"]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)