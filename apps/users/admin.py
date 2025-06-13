from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'telegram_id', 'full_name', 'phone_number', 'language', 'is_active')
    list_filter = ('language', 'is_active')
    search_fields = ('telegram_id', 'full_name', 'phone_number')
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('telegram_id', 'full_name', 'phone_number', 'language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telegram_id', 'full_name', 'phone_number', 'language')}
         ),
    )
