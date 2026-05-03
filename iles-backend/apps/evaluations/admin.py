from django.contrib import admin

from .models import Evaluation, EvaluationCriterion


@admin.register(EvaluationCriterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ("name", "weight_percent", "is_active")
    search_fields = ("name",)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("weekly_log", "evaluator", "total_score", "created_at")
    search_fields = ("weekly_log__student__full_name", "remarks")
    autocomplete_fields = ("weekly_log", "evaluator")
    readonly_fields = ("total_score", "created_at", "updated_at")
