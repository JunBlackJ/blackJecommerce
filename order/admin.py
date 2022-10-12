from django.contrib import admin
from order.models import ShopCart, Order, OrderProduct

# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter = ['user']

class OrderProductLine(admin.TabularInline):
	model = OrderProduct
	readonly_fields = ('user', 'product', 'price', 'quantity', 'amount', 'status')
	can_delete = False
	extra = 0
		

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'phone', 'city', 'total', 'status', 'code']
    list_filter = ['status']
    readonly_fields = ('user', 'first_name', 'last_name', 'phone', 'city', 'total', 'code')
    can_delete = False
    inlines = [OrderProductLine]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['status', 'product', 'user', 'quantity', 'price', 'amount']
    list_filter = ['user']

admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)