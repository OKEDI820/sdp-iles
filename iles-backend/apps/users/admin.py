from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "full_name", "role", "department", "is_active")
    list_filter = ("role", "is_active", "department")
    search_fields = ("email", "full_name", "student_number", "staff_number")
    ordering = ("full_name",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Profile", {"fields": ("full_name", "first_name", "last_name", "phone")}),
        ("Role", {"fields": ("role", "department", "student_number", "staff_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
                                     "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2",
                       "role", "full_name", "department"),
        }),
    )
