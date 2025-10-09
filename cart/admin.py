from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    readonly_fields = ('total_items', 'total_price')

    def total_items(self, obj):
        return obj.total_items()
    total_items.short_description = 'تعداد آیتم‌ها'

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'جمع کل'

admin.site.register(Cart, CartAdmin)
