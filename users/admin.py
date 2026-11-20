from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'full_name',
        'email',
        'phone_number',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'full_name',
        'email',
        'phone_number',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('PowerWatch Information', {
            'fields': ('phone_number', 'full_name', 'created_at'),
        }),
    )

    readonly_fields = ('created_at',)
