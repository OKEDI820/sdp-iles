from django.contrib import admin

from .models import InternshipPlacement


@admin.register(InternshipPlacement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("student", "company_name", "status", "start_date", "end_date")
    list_filter = ("status",)
    search_fields = ("student__full_name", "company_name")
    autocomplete_fields = ("student", "workplace_supervisor", "academic_supervisor")
