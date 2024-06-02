from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = ('password', 'date_joined', 'last_login', 'groups', 'user_permissions')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'image')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'image')}),
    )