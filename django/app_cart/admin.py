from django.contrib import admin
from .models import Category, Order, Product, OrderItem


# admin.py
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ("id", "customer", "created_at")
    inlines = [OrderItemInline]


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
