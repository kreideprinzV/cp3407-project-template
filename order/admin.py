from django.contrib import admin

from order.models import Order, OrderItem, Table
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Table)

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'unit_price', 'line_total')

