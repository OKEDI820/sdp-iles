from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'full_name', 'role', 'is_active')
    ordering = ('id',)
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role', 'full_name')}),)
