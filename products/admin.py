from django.contrib import admin
from .models import Product, Category, Invoice, Invoice_Cart

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base Admin
    list_display = ('title', 'ar_title', 'slug', 'content')
    search_fields = ('title', 'slug')


class ProductAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    list_display = ('title', 'ar_title', 'category', 'price',
                    'createdBy', 'createdAt', 'updatedAt')
    search_fields = ('title', 'createdBy')
    ordering = ('-createdAt',)
    list_filter = ('category',)


class TransactionAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    list_display = ('invoiceId', 'total',
                    'payment_type', 'createdBy', 'createdAt', 'updatedAt', 'slug')
    search_fields = ('total', 'createdBy__email', 'createdAt')
    ordering = ('-createdAt',)
    list_filter = ('createdBy', 'payment_type',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice, TransactionAdmin)
admin.site.register(Invoice_Cart)
