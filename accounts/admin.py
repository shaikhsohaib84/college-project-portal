from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('department',)}),
    )
    list_display = BaseUserAdmin.list_display + ('department',)

admin.site.register(User, UserAdmin)