from django.contrib import admin

from .models import WeeklyLog


@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ("week_number", "student", "status", "submission_deadline", "submitted_at")
    list_filter = ("status",)
    search_fields = ("title", "student__full_name", "placement__company_name")
    autocomplete_fields = ("student", "placement", "reviewed_by", "approved_by")
    readonly_fields = ("submitted_at", "reviewed_at", "approved_at", "rejected_at",
                       "created_at", "updated_at")
