from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vendor, Product, Order, OrderItem

# Register the custom User model with the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # add the 'role' field to the default UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the rest of the models simply
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
